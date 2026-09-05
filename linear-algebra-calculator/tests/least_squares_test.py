import pytest
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.algorithms.least_squares import least_squares
from app.exceptions import LinearDependenceError

def test_least_squares():
    A = Matrix([
        [1, 0],
        [1, 1],
        [1, 2]
    ])
    b = Vector([
        1,
        2,
        2
    ])
    result = least_squares(A, b)

    assert result.data == pytest.approx(
        [1.1666666667, 0.5]
    )

def test_least_squares_exact_solution():
    A = Matrix([
        [1, 0],
        [1, 1],
        [1, 2]
    ])
    b = Vector([
        1,
        3,
        5
    ])
    result = least_squares(A, b)

    assert result.data == pytest.approx([
        1.0,
        2.0
    ])

def test_least_squares_dependent_columns():
    A = Matrix([
        [1, 2],
        [2, 4],
        [3, 6]
    ])
    b = Vector([
        1,
        2,
        3
    ])

    with pytest.raises(LinearDependenceError):
        least_squares(A, b)

def test_least_squares_qr_result():
    A = Matrix([
        [1, 0],
        [1, 1],
        [1, 2]
    ])
    b = Vector([
        1,
        2,
        2
    ])
    result = least_squares(A, b)

    assert result.data == pytest.approx([
        1.1666666667,
        0.5
    ])