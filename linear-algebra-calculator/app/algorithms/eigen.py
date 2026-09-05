import cmath
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import multiply
from app.algorithms.inverse import inverse
from app.algorithms.elimination import rref
from app.algorithms.decompositions import qr_decomposition
from app.exceptions import NonSquareMatrixError
from app.utils.numeric import clean_number, is_zero, is_close, clean_complex
from app.exceptions import LinearDependenceError, SingularMatrixError

def eigenvalues(A, max_iterations=1000):
    if A.rows != A.columns:
        raise NonSquareMatrixError

    # Keep exact 2x2 handling
    if A.rows == 2:
        a = A[0][0]
        b = A[0][1]
        c = A[1][0]
        d = A[1][1]

        trace = a + d
        det = a * d - b * c
        discriminant = trace ** 2 - 4 * det

        sqrt_discriminant = cmath.sqrt(discriminant)

        lambda1 = (trace + sqrt_discriminant) / 2
        lambda2 = (trace - sqrt_discriminant) / 2

        return [clean_complex(lambda1), clean_complex(lambda2),]

    # General n x n real eigenvalues using QR iteration
    current = A.copy()

    for _ in range(max_iterations):
        Q, R = qr_decomposition(current)
        current = multiply(R, Q)

        converged = True

        for row in range(1, current.rows):
            for column in range(row):
                if not is_zero(current[row][column]):
                    converged = False
                    break
            if not converged:
                break
        if converged:
            break
    else:
        raise ValueError("Eigenvalue iteration did not converge.")

    return [clean_number(current[i][i]) for i in range(current.rows)]

def eigenvectors(A):
    values = eigenvalues(A)
    vectors = []
    processed = []

    for eigenvalue in values:
        already_processed = any(is_close(eigenvalue, processed_value) for processed_value in processed)

        if already_processed:
            continue

        basis = eigenspace_basis(A, eigenvalue)
        vectors.extend(basis)
        processed.append(eigenvalue)

    return vectors

def diagonalize(A):
    values = eigenvalues(A)
    vectors = eigenvectors(A)

    if len(vectors) != A.columns:
        raise LinearDependenceError

    P = Matrix([
        [vectors[column][row] for column in range(len(vectors))]
        for row in range(A.rows)])

    try:
        P_inverse = inverse(P)
    except SingularMatrixError:
        raise LinearDependenceError

    D = Matrix([
        [values[row] if row == column else 0.0
            for column in range(A.columns)]
        for row in range(A.rows)])

    return P, D, P_inverse

def eigenvector_for_value(A: Matrix, eigenvalue):
    n = A.rows

    shifted = Matrix([
        [A[row][column]
            - (eigenvalue if row == column else 0.0)
            for column in range(n)]
        for row in range(n)])

    reduced = rref(shifted)

    pivot_columns = []

    for row in range(reduced.rows):
        for column in range(reduced.columns):
            if not is_zero(reduced[row][column]):
                pivot_columns.append(column)
                break

    free_columns = [
        column
        for column in range(n)
        if column not in pivot_columns]

    if not free_columns:
        raise ValueError("Could not determine an eigenvector.")

    free_column = free_columns[-1]

    vector = [0.0] * n
    vector[free_column] = 1.0

    for row in range(reduced.rows - 1, -1, -1):
        pivot_column = None

        for column in range(n):
            if not is_zero(reduced[row][column]):
                pivot_column = column
                break

        if pivot_column is None:
            continue

        total = 0.0

        for column in range(pivot_column + 1, n):
            total += (reduced[row][column] * vector[column])

        vector[pivot_column] = -total

    return Vector(vector)

def eigenspace_basis(A: Matrix, eigenvalue):
    n = A.rows

    shifted = Matrix([
        [A[row][column]
            - (eigenvalue if row == column else 0.0)
            for column in range(n)]
        for row in range(n)])

    reduced = rref(shifted)

    pivot_columns = []

    for row in range(reduced.rows):
        for column in range(n):
            if not is_zero(reduced[row][column]):
                pivot_columns.append(column)
                break

    free_columns = [
        column
        for column in range(n)
        if column not in pivot_columns]

    basis = []

    for free_column in free_columns:
        vector = [0.0] * n
        vector[free_column] = 1.0

        for row in range(reduced.rows - 1, -1, -1):
            pivot_column = None

            for column in range(n):
                if not is_zero(reduced[row][column]):
                    pivot_column = column
                    break

            if pivot_column is None:
                continue

            total = 0.0

            for column in range(pivot_column + 1, n):
                total += (
                    reduced[row][column]
                    * vector[column])

            vector[pivot_column] = -total

        basis.append(Vector(vector))

    return basis