from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import transpose, multiply
from app.algorithms.gram_schmidt import gram_schmidt
from app.core.basic_vector_operations import norm
from app.utils.numeric import is_zero
from app.exceptions import LinearDependenceError, NonSquareMatrixError, SingularMatrixError

def qr_decomposition(A: Matrix):
    columns = [Vector([A[row][col] for row in range(A.rows)])
        for col in range(A.columns)]
    orthogonal = gram_schmidt(columns)
    orthonormal = []

    for vector in orthogonal:
        magnitude = norm(vector)
        if is_zero(magnitude):
            raise LinearDependenceError
        orthonormal.append(
            Vector([value / magnitude
                for value in vector.data]))

    Q = Matrix([
        [orthonormal[col][row]
            for col in range(len(orthonormal))]
        for row in range(A.rows)])

    R = multiply(transpose(Q), A)
    return Q, R

def lu_decomposition(A: Matrix):
    if A.rows != A.columns:
        raise NonSquareMatrixError

    n = A.rows
    L = Matrix([
        [0.0 for _ in range(n)]
        for _ in range(n)])
    U = A.copy()

    for i in range(n):
        L[i][i] = 1.0

    for pivot in range(n):
        pivot_value = U[pivot][pivot]
        if is_zero(pivot_value):
            raise SingularMatrixError
        for row in range(pivot + 1, n):
            multiplier = U[row][pivot] / pivot_value
            L[row][pivot] = multiplier
            for column in range(pivot, n):
                U[row][column] -= (multiplier * U[pivot][column])

    return L, U