from app.core.matrix import Matrix
from app.core.basic_operations import multiply, transpose
from app.algorithms.decompositions import qr_decomposition

def test_qr_reconstructs_matrix():
    A = Matrix([
        [1, 1],
        [1, 0]
    ])

    Q, R = qr_decomposition(A)
    reconstructed = multiply(Q, R)

    for i in range(A.rows):
        for j in range(A.columns):
            assert abs(reconstructed[i][j] - A[i][j]) < 1e-10

def test_q_columns_are_orthonormal():
    A = Matrix([
        [1, 1],
        [1, 0]
    ])
    Q, R = qr_decomposition(A)
    result = multiply(transpose(Q), Q)

    assert abs(result[0][0] - 1) < 1e-10
    assert abs(result[1][1] - 1) < 1e-10
    assert abs(result[0][1]) < 1e-10
    assert abs(result[1][0]) < 1e-10

def test_r_is_upper_triangular():
    A = Matrix([
        [1, 1],
        [1, 0]
    ])
    Q, R = qr_decomposition(A)

    assert abs(R[1][0]) < 1e-10