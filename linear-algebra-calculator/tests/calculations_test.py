import pytest

from app.core.matrix import Matrix
from app.core.basic_operations import multiply
from app.ui.calculations import CalculationController, CalculationResult


@pytest.mark.parametrize("operation, expected", [
    ("Addition", [[4, 2], [0, 6]]),
    ("Subtraction", [[0, 0], [0, 0]]),
    ("Scalar Multiplication", [[4, 2], [0, 6]]),
    ("Matrix Multiplication", [[4, 5], [0, 9]]),
    ("Transpose", [[2, 0], [1, 3]]),
    ("Gaussian Elimination", [[2, 1], [0, 3]]),
    ("RREF", [[1, 0], [0, 1]]),
    ("Inverse", [[0.5, -1 / 6], [0, 1 / 3]]),
    ("Gram-Schmidt", [[2, 0], [0, 3]]),
])
def test_calculate_matrix_operations(operation, expected):
    matrix = Matrix([[2, 1], [0, 3]])
    result = CalculationController().calculate(operation, matrix, matrix, scalar=2)
    assert isinstance(result, CalculationResult)
    assert result.result.rows == len(expected)
    for actual, row in zip(result.result.data, expected):
        assert actual == pytest.approx(row)
    assert matrix.data == [[2, 1], [0, 3]]


@pytest.mark.parametrize("operation, labels", [
    ("LU Decomposition", ["P", "L", "U"]),
    ("QR Decomposition", ["Q", "R"]),
    ("Diagonalization", ["P", "D", "P⁻¹"]),
])
def test_calculate_decompositions(operation, labels):
    matrix = Matrix([[2, 1], [0, 3]])
    result = CalculationController().calculate(operation, matrix)
    assert [label for label, _ in result.extra_results] == labels
    factors = [factor for _, factor in result.extra_results]
    if operation == "LU Decomposition":
        expected = multiply(factors[0], matrix)
        actual = multiply(factors[1], factors[2])
    elif operation == "QR Decomposition":
        expected = matrix
        actual = multiply(*factors)
    else:
        expected = matrix
        actual = multiply(multiply(factors[0], factors[1]), factors[2])
    for actual_row, expected_row in zip(actual.data, expected.data):
        assert actual_row == pytest.approx(expected_row)
    assert result.steps
    assert all(step.description for step in result.steps)


def test_calculate_scalar_and_eigen_results():
    controller = CalculationController()
    matrix = Matrix([[2, 0], [0, 3]])
    assert controller.calculate("Determinant", matrix).result == 6
    assert sorted(controller.calculate("Eigenvalues", matrix).result) == [2, 3]
    vectors = controller.calculate("Eigenvectors", matrix)
    assert len(vectors.result) == 2
    assert vectors.steps


def test_calculate_missing_input_and_unknown_operation():
    controller = CalculationController()
    assert controller.calculate("Addition", None) is None
    with pytest.raises(ValueError, match="Unknown operation"):
        controller.calculate("Invalid", Matrix([[1]]))


def test_calculation_result_defaults_are_independent():
    first, second = CalculationResult(1), CalculationResult(2)
    first.steps.append("step")
    first.extra_results.append(("A", Matrix([[1]])))
    assert second.steps == []
    assert second.extra_results == []
