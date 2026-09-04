import pytest
from app.algorithms.inverse import inverse
from app.algorithms.elimination import rref
from app.core.matrix import Matrix
from app.exceptions import NonSquareMatrixError, SingularMatrixError

def test_inverse_3x3():
    matrix = Matrix([
        [1, 0, 0],
        [0, 2, 0],
        [0, 0, 4]
    ])
    result = inverse(matrix)
    expected = [
        [1.0, 0.0, 0.0],
        [0.0, 0.5, 0.0],
        [0.0, 0.0, 0.25]
    ]

    for actual_row, expected_row in zip(result.data, expected):
        assert actual_row == pytest.approx(expected_row)

def test_inverse_3x3():
    matrix = Matrix([
        [1, 0, 0],
        [0, 2, 0],
        [0, 0, 4]
    ])
    result = inverse(matrix)
    expected = [
        [1.0, 0.0, 0.0],
        [0.0, 0.5, 0.0],
        [0.0, 0.0, 0.25]
    ]

    for actual_row, expected_row in zip(result.data, expected):
        assert actual_row == pytest.approx(expected_row)

def test_inverse_singular():
    matrix = Matrix([
        [1, 2],
        [2, 4]
    ])

    with pytest.raises(SingularMatrixError):
        inverse(matrix)

def test_inverse_rectangular():
    matrix = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(NonSquareMatrixError):
        inverse(matrix)

def test_inverse_1x1():
    matrix = Matrix([
        [5]
    ])
    result = inverse(matrix)
    expected = [
        [0.2]
    ]

    for actual_row, expected_row in zip(result.data, expected):
            assert actual_row == pytest.approx(expected_row)

