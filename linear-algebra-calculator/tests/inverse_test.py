import pytest
from app.algorithms.elimination import rref
from app.core.matrix import Matrix

def inverse(matrix):
    if matrix.rows != matrix.columns:
        raise ValueError("Inverse requires a square matrix.")
    n = matrix.rows

    # Create augmented matrix [A | I]
    augmented_data = []
    for i in range(n):
        row = matrix[i][:]
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        augmented_data.append(row)
    augmented = Matrix(augmented_data)

    # Reduce [A | I] to [I | A^-1]
    reduced = rref(augmented)

    # Verify left side is the identity matrix
    for i in range(n):
        for j in range(n):
            expected = 1.0 if i == j else 0.0
            if abs(reduced[i][j] - expected) > 1e-10:
                raise ValueError("Matrix is not invertible.")

    # Extract right half
    inverse_data = []
    for i in range(n):
        inverse_data.append(
            reduced[i][n:]
        )

    return Matrix(inverse_data)

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

    with pytest.raises(ValueError):
        inverse(matrix)

def test_inverse_rectangular():
    matrix = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(ValueError):
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

