import pytest
from app.core.matrix import Matrix
from app.algorithms.determinant import determinant


def test_determinant_1x1():
    matrix = Matrix([
        [5]
    ])

    assert determinant(matrix) == pytest.approx(5.0)

def test_determinant_2x2():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])

    assert determinant(matrix) == pytest.approx(-2.0)

def test_determinant_3x3():
    matrix = Matrix([
        [1, 2, 3],
        [0, 1, 4],
        [5, 6, 0]
    ])

    assert determinant(matrix) == pytest.approx(1.0)

def test_determinant_row_swap():
    matrix = Matrix([
        [0, 1],
        [1, 0]
    ])

    assert determinant(matrix) == pytest.approx(-1.0)

def test_determinant_singular():
    matrix = Matrix([
        [1, 2],
        [2, 4]
    ])

    assert determinant(matrix) == pytest.approx(0.0)

def test_determinant_rectangular():
    matrix = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(ValueError):
        determinant(matrix)