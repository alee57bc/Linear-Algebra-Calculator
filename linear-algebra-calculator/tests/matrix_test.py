import pytest
from app.core.matrix import Matrix

def test_matrix_dimensions():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    assert matrix.rows == 2
    assert matrix.columns == 2

def test_matrix_values():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    assert matrix[0][0] == 1
    assert matrix[0][1] == 2
    assert matrix[1][0] == 3
    assert matrix[1][1] == 4

def test_matrix_modification():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    matrix[0][0] = 5
    assert matrix[0][0] == 5

def test_matrix_rejects_empty_data():
    with pytest.raises(ValueError):
        Matrix([])

def test_matrix_rejects_empty_rows():
    with pytest.raises(ValueError):
        Matrix([[]])

def test_matrix_rejects_unequal_row_lengths():
    with pytest.raises(ValueError):
        Matrix([
            [1, 2],
            [3]
        ])

def test_matrix_rejects_non_list_data():
    with pytest.raises(TypeError):
        Matrix("not a matrix")

def test_matrix_rejects_non_list_rows():
    with pytest.raises(TypeError):
        Matrix([
            [1, 2],
            (3, 4)
        ])

def test_matrix_rejects_non_numeric_values():
    with pytest.raises(ValueError):
        Matrix([
            [1, 2],
            [3, "hello"]
        ])