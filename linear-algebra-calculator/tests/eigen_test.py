import pytest
from app.core.matrix import Matrix
from app.exceptions import NonSquareMatrixError, LinearDependenceError
from app.algorithms.eigen import eigenvalues, eigenvectors, diagonalize, eigenvector_for_value
from app.core.basic_operations import multiply, matrix_vector_multiply
from app.utils.numeric import is_zero, is_close

def test_eigenvalues_diagonal_matrix():
    A = Matrix([
        [2, 0],
        [0, 3]
    ])
    result = eigenvalues(A)

    assert set(result) == {2.0, 3.0}

def test_eigenvalues_non_diagonal():
    A = Matrix([
        [4, 1],
        [2, 3]
    ])
    result = eigenvalues(A)

    assert set(result) == {5.0, 2.0}

def test_eigenvalues_repeated():
    A = Matrix([
        [2, 1],
        [0, 2]
    ])
    result = eigenvalues(A)

    assert result == [2.0, 2.0]

import pytest

from app.exceptions import NonSquareMatrixError


def test_eigenvalues_requires_square_matrix():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(NonSquareMatrixError):
        eigenvalues(A)

def test_eigenvalues_requires_square_matrix():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(NonSquareMatrixError):
        eigenvalues(A)

def test_eigenvectors_diagonal_matrix():
    A = Matrix([
        [2, 0],
        [0, 3]
    ])
    values = eigenvalues(A)
    vectors = eigenvectors(A)

    assert len(vectors) == 2

    for eigenvalue, vector in zip(values, vectors):
        Av = matrix_vector_multiply(A, vector)
        expected = [eigenvalue * value for value in vector.data]

        assert Av.data == pytest.approx(expected)

def test_eigenvectors_non_diagonal():
    A = Matrix([
        [4, 1],
        [2, 3]
    ])
    values = eigenvalues(A)
    vectors = eigenvectors(A)

    for eigenvalue, vector in zip(values, vectors):
        Av = matrix_vector_multiply(A, vector)
        expected = [eigenvalue * value for value in vector.data]

        assert Av.data == pytest.approx(expected)

def test_eigenvectors_repeated_eigenvalue():
    A = Matrix([
        [2, 1],
        [0, 2]
    ])
    vectors = eigenvectors(A)

    assert len(vectors) == 2

def test_diagonalization_reconstructs_matrix():
    A = Matrix([
        [4, 1],
        [2, 3]
    ])
    P, D, P_inverse = diagonalize(A)
    reconstructed = multiply(multiply(P, D), P_inverse)

    for i in range(A.rows):
        for j in range(A.columns):
            assert is_close(reconstructed[i][j], A[i][j])

def test_diagonal_matrix_is_diagonal():
    A = Matrix([
        [4, 1],
        [2, 3]
    ])
    P, D, P_inverse = diagonalize(A)

    assert is_zero(D[0][1])
    assert is_zero(D[1][0])

def test_non_diagonalizable_matrix():
    A = Matrix([
        [2, 1],
        [0, 2]
    ])

    with pytest.raises(LinearDependenceError):
        diagonalize(A)

def test_eigenvectors_3x3_diagonal():
    A = Matrix([
        [2, 0, 0],
        [0, 3, 0],
        [0, 0, 5]
    ])

    values = eigenvalues(A)
    vectors = eigenvectors(A)

    for eigenvalue, vector in zip(values, vectors):
        Av = matrix_vector_multiply(A, vector)

        expected = [eigenvalue * value
            for value in vector.data]

        assert Av.data == pytest.approx(expected)

def test_eigenvalues_3x3_triangular():
    A = Matrix([
        [1, 4, 2],
        [0, 3, 5],
        [0, 0, 6]
    ])
    result = eigenvalues(A)

    assert set(result) == {1.0, 3.0, 6.0}

def test_complex_eigenvectors():
    A = Matrix([
        [0, -1],
        [1, 0]
    ])
    values = eigenvalues(A)
    vectors = eigenvectors(A)

    for eigenvalue, vector in zip(values, vectors):
        Av = matrix_vector_multiply(A, vector)
        expected = [eigenvalue * value
            for value in vector.data]

        assert Av.data == pytest.approx(expected)