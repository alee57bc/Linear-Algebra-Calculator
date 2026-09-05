import pytest
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import add,multiply, transpose, matrix_vector_multiply
from app.algorithms.inverse import inverse
from app.algorithms.elimination import rref, rank
from app.algorithms.determinant import determinant
from app.algorithms.decompositions import qr_decomposition, lu_decomposition
from app.algorithms.eigen import eigenvalues, eigenvectors, diagonalize
from app.algorithms.least_squares import least_squares
from app.utils.numeric import is_close, is_zero

def assert_matrix_close(A, B):
    assert A.rows == B.rows
    assert A.columns == B.columns

    for i in range(A.rows):
        for j in range(A.columns):
            assert is_close(A[i][j], B[i][j])

def identity(n):
    return Matrix([
        [
            1.0 if i == j else 0.0
            for j in range(n)
        ]
        for i in range(n)
    ])

def test_addition_is_commutative():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])
    B = Matrix([
        [5, 6],
        [7, 8]
    ])
    assert_matrix_close(
        add(A, B),
        add(B, A)
    )

def test_transpose_twice_returns_original():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])
    assert_matrix_close(
        transpose(transpose(A)),
        A
    )

def test_matrix_identity_property():
    A = Matrix([
        [2, 3],
        [4, 5]
    ])
    I = identity(2)
    assert_matrix_close(multiply(A, I), A)

def test_inverse_property():
    A = Matrix([
        [4, 7],
        [2, 6]
    ])
    A_inverse = inverse(A)
    result = multiply(A, A_inverse)

    assert_matrix_close(result, identity(2))

def test_rref_is_idempotent():
    A = Matrix([
        [1, 2, 3],
        [2, 4, 7]
    ])
    first = rref(A)
    second = rref(first)
    assert_matrix_close(first, second)

def test_rank_equals_transpose_rank():
    A = Matrix([
        [1, 2, 3],
        [2, 4, 6]
    ])
    assert rank(A) == rank(transpose(A))

def test_determinant_multiplication_property():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])
    B = Matrix([
        [2, 0],
        [1, 3]
    ])
    AB = multiply(A, B)

    assert is_close(determinant(AB), determinant(A) * determinant(B))

def test_qr_properties():
    A = Matrix([
        [1, 1],
        [1, 0]
    ])
    Q, R = qr_decomposition(A)
    assert_matrix_close(multiply(Q, R), A)
    assert_matrix_close(multiply(transpose(Q), Q), identity(Q.columns))

def test_lu_property():
    A = Matrix([
        [0, 1],
        [1, 1]
    ])
    P, L, U = lu_decomposition(A)
    assert_matrix_close(multiply(P, A), multiply(L, U))

def test_eigenvector_property():
    A = Matrix([
        [4, 1],
        [2, 3]
    ])
    values = eigenvalues(A)
    vectors = eigenvectors(A)

    # Distinct eigenvalues here, so one vector per value.
    for eigenvalue, vector in zip(values, vectors):
        Av = matrix_vector_multiply(A, vector)
        expected = Vector([
            eigenvalue * value
            for value in vector.data])
        for actual, expected_value in zip(Av.data, expected.data):
            assert is_close(actual, expected_value)

def test_diagonalization_property():
    A = Matrix([
        [4, 1],
        [2, 3]
    ])
    P, D, P_inverse = diagonalize(A)
    reconstructed = multiply(multiply(P, D), P_inverse)
    assert_matrix_close(reconstructed, A)

def test_least_squares_normal_residual_property():
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
    x = least_squares(A, b)
    Ax = matrix_vector_multiply(A, x)
    residual = Vector([
        b[i] - Ax[i]
        for i in range(b.dimension)])
    normal_residual = matrix_vector_multiply(transpose(A), residual)

    for value in normal_residual.data:
        assert is_zero(value)