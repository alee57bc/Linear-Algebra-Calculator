from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import transpose, multiply
from app.algorithms.gram_schmidt import gram_schmidt
from app.algorithms.elimination import swap_rows
from app.core.basic_vector_operations import norm
from app.utils.numeric import is_zero, clean_number, format_number
from app.exceptions import LinearDependenceError, NonSquareMatrixError, SingularMatrixError
from app.results.calculation_step import CalculationStep

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

    P = Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])

    for i in range(n):
        L[i][i] = 1.0

    if steps is not None:
        steps.append(CalculationStep(description="Start with U = A.", result=U.copy()))

    for pivot in range(n):
        pivot_row = None

        for row in range(pivot, n):
            if not is_zero(U[row][pivot]):
                pivot_row = row
                break

        if pivot_row is None:
            raise SingularMatrixError

        if steps is not None:
            steps.append(CalculationStep(description=(f"Use {format_number(U[pivot_row][pivot])} " f"as the pivot in column {pivot + 1}."), result=U.copy()))

        if pivot_row != pivot:
            swap_rows(U, pivot, pivot_row)
            swap_rows(P, pivot, pivot_row)

            # Only swap the part of L that has already been built
            for column in range(pivot):
                L[pivot][column], L[pivot_row][column] = (L[pivot_row][column], L[pivot][column],)

            if steps is not None:
                steps.append(CalculationStep(description=(f"Swap R{pivot + 1} and R{pivot_row + 1}"), result=U.copy(),))

        pivot_value = U[pivot][pivot]

        for row in range(pivot + 1, n):
            multiplier = U[row][pivot] / pivot_value
            L[row][pivot] = multiplier

            if steps is not None:
                steps.append(CalculationStep(description=(
                            f"Compute multiplier "
                            f"m{row + 1}{pivot + 1} = "
                            f"{format_number(U[row][pivot])} / "
                            f"{format_number(pivot_value)} = "
                            f"{format_number(multiplier)}."),
                        result=L.copy()))

            for column in range(pivot, n):
                U[row][column] -= (multiplier * U[pivot][column])

            if steps is not None:
                steps.append(CalculationStep(description=(f"R{row + 1} ← R{row + 1} " f"- ({format_number(multiplier)})R{pivot + 1}"), result=U.copy(),))

    if steps is not None:
        steps.append(CalculationStep(description="Final permutation matrix P.", result=P.copy()))
        steps.append(CalculationStep(description="Final lower triangular matrix L.", result=L.copy()))
        steps.append(CalculationStep(description="Final upper triangular matrix U.", result=U.copy()))

    if record_steps:
        return P, L, U, steps

    return P, L, U