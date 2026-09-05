import pytest

from app.algorithms.decompositions import lu_decomposition, qr_decomposition
from app.algorithms.determinant import determinant
from app.algorithms.eigen import eigenvalues, eigenvectors, eigenvector_for_value, eigenspace_basis
from app.algorithms.elimination import gaussian_elimination, rref
from app.algorithms.gram_schmidt import gram_schmidt
from app.algorithms.inverse import inverse
from app.algorithms.least_squares import least_squares
from app.core.basic_operations import multiply, transpose, matrix_vector_multiply
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.exceptions import DimensionMismatchError, LinearDependenceError, SingularMatrixError
from app.ui.calculations import CalculationController


def assert_matrix_close(actual, expected):
    assert (actual.rows, actual.columns) == (expected.rows, expected.columns)
    for actual_row, expected_row in zip(actual.data, expected.data):
        assert actual_row == pytest.approx(expected_row)


@pytest.mark.parametrize("data", [[[0, 1], [0, 2]], [[1, 2], [2, 4]]])
def test_singular_determinant_records_steps(data):
    matrix = Matrix(data)
    value, steps = determinant(matrix, record_steps=True)
    assert value == 0
    assert isinstance(steps, list)
    assert CalculationController().calculate("Determinant", matrix).result == 0


def test_determinant_records_swap_and_preserves_input():
    matrix = Matrix([[0, 2], [3, 4]])
    value, steps = determinant(matrix, record_steps=True)
    assert value == -6
    assert steps[0].result == Matrix([[3, 4], [0, 2]])
    assert matrix == Matrix([[0, 2], [3, 4]])


def test_lu_later_pivot_swaps_existing_multipliers():
    matrix = Matrix([[1, 1, 0], [2, 2, 1], [3, 4, 1]])
    p, lower, upper, steps = lu_decomposition(matrix, record_steps=True)
    assert lower[1][0] == 3
    assert lower[2][0] == 2
    assert_matrix_close(multiply(p, matrix), multiply(lower, upper))
    assert steps[0].result == matrix
    assert steps[-3].result == p
    assert steps[-2].result == lower
    assert steps[-1].result == upper
    upper[0][0] = 99
    assert steps[-1].result[0][0] == 1
    assert matrix[0][0] == 1


@pytest.mark.parametrize("record_steps", [False, True])
def test_lu_rejects_singular_matrix(record_steps):
    with pytest.raises(SingularMatrixError):
        lu_decomposition(Matrix([[1, 2], [2, 4]]), record_steps=record_steps)


def test_rectangular_qr_reconstruction_and_orthonormality():
    matrix = Matrix([[1, 1], [1, 0], [0, 1]])
    q, r, steps = qr_decomposition(matrix, record_steps=True)
    assert_matrix_close(multiply(q, r), matrix)
    assert_matrix_close(multiply(transpose(q), q), Matrix([[1, 0], [0, 1]]))
    assert steps[-2].result == q
    assert steps[-1].result == r
    q[0][0] = 99
    assert steps[-2].result[0][0] != 99


@pytest.mark.parametrize("vectors", [[[0, 0]], [[1, 2], [2, 4]]])
def test_gram_schmidt_rejects_dependent_vectors(vectors):
    with pytest.raises(LinearDependenceError):
        gram_schmidt([Vector(values) for values in vectors])


def test_dimension_mismatches():
    matrix, vector = Matrix([[1, 0], [0, 1]]), Vector([1, 2, 3])
    with pytest.raises(DimensionMismatchError):
        matrix_vector_multiply(matrix, vector)
    with pytest.raises(DimensionMismatchError):
        least_squares(matrix, vector)
    with pytest.raises(DimensionMismatchError):
        gram_schmidt([Vector([1, 0]), vector])


@pytest.mark.parametrize("operation", [gaussian_elimination, rref])
def test_elimination_skips_zero_columns_and_rows(operation):
    matrix = Matrix([[0, 1, 2], [0, 0, 0], [0, 2, 4]])
    result, steps = operation(matrix, record_steps=True)
    assert result == Matrix([[0, 1, 2], [0, 0, 0], [0, 0, 0]])
    assert steps
    snapshot = steps[0].result.copy()
    result[0][1] = 99
    assert steps[0].result == snapshot
    assert matrix == Matrix([[0, 1, 2], [0, 0, 0], [0, 2, 4]])


def test_inverse_steps_end_with_augmented_identity_and_inverse():
    matrix = Matrix([[0, 2], [1, 3]])
    result, steps = inverse(matrix, record_steps=True)
    assert_matrix_close(multiply(matrix, result), Matrix([[1, 0], [0, 1]]))
    assert steps[-1].result == Matrix([[1, 0, -1.5, 1], [0, 1, 0.5, 0]])


@pytest.mark.parametrize("data, value", [
    ([[4, 1], [2, 3]], 5),
    ([[2, 0], [0, 2]], 2),
    ([[0, -1], [1, 0]], 1j),
])
def test_eigenvector_for_value_satisfies_equation(data, value):
    matrix = Matrix(data)
    vector = eigenvector_for_value(matrix, value)
    assert any(abs(entry) > 1e-10 for entry in vector.data)
    assert matrix_vector_multiply(matrix, vector).data == pytest.approx(
        [value * entry for entry in vector.data])


def test_value_outside_spectrum_has_no_eigenspace():
    matrix = Matrix([[2, 0], [0, 3]])
    assert eigenspace_basis(matrix, 7) == []
    with pytest.raises(ValueError, match="Could not determine"):
        eigenvector_for_value(matrix, 7)


def test_repeated_eigenvalue_returns_full_basis():
    vectors, steps = eigenvectors(Matrix([[2, 0], [0, 2]]), record_steps=True)
    assert [vector.data for vector in vectors] == [[1, 0], [0, 1]]
    assert steps[-1].result.data == vectors[-1].data
    vectors[-1][0] = 99
    assert steps[-1].result[0] == 0


def test_qr_eigenvalue_iteration_converges_and_records_result():
    values, steps = eigenvalues(Matrix([[2, 1, 0], [1, 2, 0], [0, 0, 4]]), record_steps=True)
    assert sorted(values) == pytest.approx([1, 3, 4])
    assert steps[-1].description == "QR iteration converged."
    assert isinstance(steps[-1].result, Matrix)


def test_qr_eigenvalue_iteration_reports_nonconvergence():
    with pytest.raises(ValueError, match="did not converge"):
        eigenvalues(Matrix([[2, 1, 0], [1, 2, 0], [0, 0, 4]]), max_iterations=0)
