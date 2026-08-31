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