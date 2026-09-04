import pytest
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import add, subtract, scalar_multiply, multiply, transpose, matrix_vector_multiply
from app.exceptions import DimensionMismatchError

# Addition
def test_addition():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6],
        [7, 8]
    ])
    result = add(a, b)

    assert result.data == [
        [6.0, 8.0],
        [10.0, 12.0]
    ]

def test_addition_dimension_mismatch():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(DimensionMismatchError):
        add(a, b)

# Subtraction
def test_subtraction():
    a = Matrix([
        [5, 6],
        [7, 8]
    ])
    b = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = subtract(a, b)

    assert result.data == [
        [4.0, 4.0],
        [4.0, 4.0]
    ]

def test_subtraction_dimension_mismatch():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(DimensionMismatchError):
        subtract(a, b)

# Scalar Multiplication
def test_scalar_multiplication_positive():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = scalar_multiply(a, 3)

    assert result.data == [
        [3.0, 6.0],
        [9.0, 12.0]
    ]

def test_scalar_multiplication_negative():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = scalar_multiply(a, -2)

    assert result.data == [
        [-2.0, -4.0],
        [-6.0, -8.0]
    ]

def test_scalar_multiplication_decimal():
    a = Matrix([
        [2, 4],
        [6, 8]
    ])
    result = scalar_multiply(a, 0.5)

    assert result.data == [
        [1.0, 2.0],
        [3.0, 4.0]
    ]

def test_scalar_multiplication_zero():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = scalar_multiply(a, 0)

    assert result.data == [
        [0.0, 0.0],
        [0.0, 0.0]
    ]

# Matrix Multiplication
def test_matrix_multiplication_2x2():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6],
        [7, 8]
    ])
    result = multiply(a, b)

    assert result.data == [
        [19.0, 22.0],
        [43.0, 50.0]
    ]

def test_matrix_multiplication_2x3_by_3x2():
    a = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])
    b = Matrix([
        [7, 8],
        [9, 10],
        [11, 12]
    ])
    result = multiply(a, b)

    assert result.data == [
        [58.0, 64.0],
        [139.0, 154.0]
    ]

def test_matrix_multiplication_3x2_by_2x3():
    a = Matrix([
        [1, 2],
        [3, 4],
        [5, 6]
    ])
    b = Matrix([
        [7, 8, 9],
        [10, 11, 12]
    ])
    result = multiply(a, b)

    assert result.data == [
        [27.0, 30.0, 33.0],
        [61.0, 68.0, 75.0],
        [95.0, 106.0, 117.0]
    ]

def test_matrix_multiplication_invalid_dimensions():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ])

    with pytest.raises(DimensionMismatchError):
        multiply(a, b)

# Transpose
def test_transpose_square():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = transpose(a)

    assert result.data == [
        [1.0, 3.0],
        [2.0, 4.0]
    ]

def test_transpose_rectangular():
    a = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])
    result = transpose(a)

    assert result.data == [
        [1.0, 4.0],
        [2.0, 5.0],
        [3.0, 6.0]
    ]

def test_transpose_1xN():
    a = Matrix([
        [1, 2, 3, 4]
    ])
    result = transpose(a)

    assert result.data == [
        [1.0],
        [2.0],
        [3.0],
        [4.0]
    ]

def test_transpose_Nx1():
    a = Matrix([
        [1],
        [2],
        [3],
        [4]
    ])
    result = transpose(a)

    assert result.data == [
        [1.0, 2.0, 3.0, 4.0]
    ]

def test_matrix_vector_multiply():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    vector = Vector([5, 6])
    result = matrix_vector_multiply(
        matrix,
        vector
    )

    assert result.data == pytest.approx([
        17.0,
        39.0
    ])