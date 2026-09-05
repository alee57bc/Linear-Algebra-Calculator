from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import transpose, multiply
from app.algorithms.gram_schmidt import gram_schmidt
from app.core.basic_vector_operations import norm
from app.utils.numeric import is_zero
from app.exceptions import LinearDependenceError, NonSquareMatrixError, SingularMatrixError
from app.results.calculation_step import CalculationStep
from app.utils.numeric import clean_number

def qr_decomposition(A, record_steps=False):
    columns = [Vector([A[row][col] for row in range(A.rows)])
        for col in range(A.columns)]

    if record_steps:
        orthogonal, steps = gram_schmidt(columns, record_steps=True)
    else:
        orthogonal = gram_schmidt(columns)
        steps = None

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

    if steps is not None:
        steps.append(CalculationStep(description="Build Q from the orthonormal vectors.", result=Q.copy()))

    R = multiply(transpose(Q), A)
    if steps is not None:
        steps.append(CalculationStep(description="Compute R = QᵀA.", result=R.copy()))

    if record_steps:
        return Q, R, steps
    return Q, R

def lu_decomposition(A, record_steps=False):
    if A.rows != A.columns:
        raise NonSquareMatrixError

    steps = [] if record_steps else None

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

            if steps is not None:
                steps.append(
                    CalculationStep(
                        description=(f"R{row + 1} ← R{row + 1} - ({multiplier})R{pivot + 1}"),
                        result=U.copy()))

    if record_steps:
        return L, U, steps

    return L, U