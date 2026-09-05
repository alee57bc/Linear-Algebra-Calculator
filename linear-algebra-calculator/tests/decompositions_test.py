import pytest
from app.core.matrix import Matrix
from app.core.basic_operations import multiply, transpose
from app.algorithms.decompositions import qr_decomposition
from app.utils.numeric import is_zero, is_close
from app.exceptions import NonSquareMatrixError, SingularMatrixError
from app.algorithms.decompositions import qr_decomposition, lu_decomposition

def test_qr_reconstructs_matrix():
    A = Matrix([
        [1, 1],
        [1, 0]
    ])

    Q, R = qr_decomposition(A)
    reconstructed = multiply(Q, R)

    for i in range(A.rows):
        for j in range(A.columns):
            assert is_close(reconstructed[i][j], A[i][j])

def test_q_columns_are_orthonormal():
    A = Matrix([
        [1, 1],
        [1, 0]
    ])
    Q, R = qr_decomposition(A)
    result = multiply(transpose(Q), Q)

    assert is_close(result[0][0], 1.0)
    assert is_close(result[1][1], 1.0)
    assert is_zero(result[0][1])
    assert is_zero(result[1][0])

def test_r_is_upper_triangular():
    A = Matrix([
        [1, 1],
        [1, 0]
    ])
    Q, R = qr_decomposition(A)

    assert is_zero(R[1][0])

def test_lu_reconstructs_matrix():
    A = Matrix([
        [2, 3],
        [4, 7]
    ])
    P, L, U = lu_decomposition(A)

    left = multiply(P, A)
    right = multiply(L, U)

    for i in range(A.rows):
        for j in range(A.columns):
            assert is_close(
                left[i][j],
                right[i][j])

def test_l_is_lower_triangular():
    A = Matrix([
        [2, 3],
        [4, 7]
    ])
    P, L, U = lu_decomposition(A)

    assert is_zero(L[0][1])
    assert is_close(L[0][0], 1.0)
    assert is_close(L[1][1], 1.0)

def test_u_is_upper_triangular():
    A = Matrix([
        [2, 3],
        [4, 7]
    ])
    P, L, U = lu_decomposition(A)

    assert is_zero(U[1][0])

def test_lu_requires_square_matrix():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])
    with pytest.raises(NonSquareMatrixError):
        lu_decomposition(A)

def test_lu_with_row_pivoting():
    A = Matrix([
        [0, 1],
        [1, 1]
    ])
    P, L, U = lu_decomposition(A)

    left = multiply(P, A)
    right = multiply(L, U)

    for i in range(A.rows):
        for j in range(A.columns):
            assert is_close(
                left[i][j],
                right[i][j])