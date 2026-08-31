import pytest
from app.core.matrix import Matrix
from app.core.operations import add, subtract, scalar_multiply, multiply, transpose

def test_add_normal_matrices():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6],
        [7, 8]
    ])
    result = add(a, b)

    assert result[0][0] == 6
    assert result[0][1] == 8
    assert result[1][0] == 10
    assert result[1][1] == 12

def test_add_negative_numbers():
    a = Matrix([
        [-1, -2],
        [-3, -4]
    ])
    b = Matrix([
        [5, 6],
        [7, 8]
    ])
    result = add(a, b)

    assert result[0][0] == 4
    assert result[0][1] == 4
    assert result[1][0] == 4
    assert result[1][1] == 4

def test_add_decimal_numbers():
    a = Matrix([
        [1.5, 2.5],
        [3.5, 4.5]
    ])
    b = Matrix([
        [0.5, 1.5],
        [2.5, 3.5]
    ])
    result = add(a, b)

    assert result[0][0] == 2.0
    assert result[0][1] == 4.0
    assert result[1][0] == 6.0
    assert result[1][1] == 8.0

def test_add_1x1_matrices():
    a = Matrix([
        [5]
    ])
    b = Matrix([
        [3]
    ])
    result = add(a, b)

    assert result.rows == 1
    assert result.columns == 1
    assert result[0][0] == 8

def test_add_dimension_mismatch():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6, 7],
        [8, 9, 10]
    ])

    with pytest.raises(ValueError):
        add(a, b)

def test_add_does_not_modify_original_matrices():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6],
        [7, 8]
    ])
    add(a, b)

    assert a[0][0] == 1
    assert a[0][1] == 2
    assert a[1][0] == 3
    assert a[1][1] == 4

    assert b[0][0] == 5
    assert b[0][1] == 6
    assert b[1][0] == 7
    assert b[1][1] == 8

def test_subtract_normal_matrices():
    a = Matrix([
        [5, 6],
        [7, 8]
    ])
    b = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = subtract(a, b)

    assert result[0][0] == 4
    assert result[0][1] == 4
    assert result[1][0] == 4
    assert result[1][1] == 4

def test_subtract_negative_numbers():
    a = Matrix([
        [-1, -2],
        [-3, -4]
    ])
    b = Matrix([
        [-5, -6],
        [-7, -8]
    ])
    result = subtract(a, b)

    assert result[0][0] == 4
    assert result[0][1] == 4
    assert result[1][0] == 4
    assert result[1][1] == 4

def test_subtract_decimal_numbers():
    a = Matrix([
        [5.5, 6.5],
        [7.5, 8.5]
    ])
    b = Matrix([
        [1.5, 2.5],
        [3.5, 4.5]
    ])
    result = subtract(a, b)

    assert result[0][0] == 4.0
    assert result[0][1] == 4.0
    assert result[1][0] == 4.0
    assert result[1][1] == 4.0

def test_subtract_dimension_mismatch():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6, 7],
        [8, 9, 10]
    ])

    with pytest.raises(ValueError):
        subtract(a, b)

def test_subtract_does_not_modify_original_matrices():
    a = Matrix([
        [5, 6],
        [7, 8]
    ])
    b = Matrix([
        [1, 2],
        [3, 4]
    ])
    subtract(a, b)

    assert a[0][0] == 5
    assert a[0][1] == 6
    assert a[1][0] == 7
    assert a[1][1] == 8

    assert b[0][0] == 1
    assert b[0][1] == 2
    assert b[1][0] == 3
    assert b[1][1] == 4

def test_scalar_multiply():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = scalar_multiply(matrix, 3)

    assert result[0][0] == 3
    assert result[0][1] == 6
    assert result[1][0] == 9
    assert result[1][1] == 12

def test_scalar_multiply_negative():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = scalar_multiply(matrix, -2)

    assert result[0][0] == -2
    assert result[0][1] == -4
    assert result[1][0] == -6
    assert result[1][1] == -8

def test_scalar_multiply_decimal():
     matrix = Matrix([
         [2, 4],
         [6, 8]
     ])
     result = scalar_multiply(matrix, 0.5)

     assert result[0][0] == 1.0
     assert result[0][1] == 2.0
     assert result[1][0] == 3.0
     assert result[1][1] == 4.0

def test_scalar_multiply_zero():
     matrix = Matrix([
         [1, 2],
         [3, 4]
     ])
     result = scalar_multiply(matrix, 0)

     assert result[0][0] == 0
     assert result[0][1] == 0
     assert result[1][0] == 0
     assert result[1][1] == 0

def test_scalar_multiply_does_not_modify_original():
     matrix = Matrix([
         [1, 2],
         [3, 4]
     ])
     scalar_multiply(matrix, 3)

     assert matrix[0][0] == 1
     assert matrix[0][1] == 2
     assert matrix[1][0] == 3
     assert matrix[1][1] == 4

def test_matrix_multiply():
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

    assert result.rows == 2
    assert result.columns == 2

    assert result[0][0] == 58
    assert result[0][1] == 64
    assert result[1][0] == 139
    assert result[1][1] == 154

def test_matrix_multiply_dimension_mismatch():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6],
        [7, 8],
        [9, 10]
    ])

    with pytest.raises(ValueError):
        multiply(a, b)

def test_matrix_multiply_1x1():
    a = Matrix([
        [5]
    ])
    b = Matrix([
        [3]
    ])
    result = multiply(a, b)

    assert result.rows == 1
    assert result.columns == 1
    assert result[0][0] == 15

def test_matrix_multiply_does_not_modify_originals():
    a = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Matrix([
        [5, 6],
        [7, 8]
    ])
    multiply(a, b)

    assert a[0][0] == 1
    assert a[0][1] == 2
    assert a[1][0] == 3
    assert a[1][1] == 4

    assert b[0][0] == 5
    assert b[0][1] == 6
    assert b[1][0] == 7
    assert b[1][1] == 8

def test_transpose():
    matrix = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])
    result = transpose(matrix)

    assert result.rows == 3
    assert result.columns == 2

    assert result[0][0] == 1
    assert result[0][1] == 4
    assert result[1][0] == 2
    assert result[1][1] == 5
    assert result[2][0] == 3
    assert result[2][1] == 6

def test_transpose_square_matrix():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = transpose(matrix)

    assert result.rows == 2
    assert result.columns == 2

    assert result[0][0] == 1
    assert result[0][1] == 3
    assert result[1][0] == 2
    assert result[1][1] == 4

def test_transpose_does_not_modify_original():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    transpose(matrix)

    assert matrix[0][0] == 1
    assert matrix[0][1] == 2
    assert matrix[1][0] == 3
    assert matrix[1][1] == 4