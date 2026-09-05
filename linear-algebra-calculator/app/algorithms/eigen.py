import cmath
import math
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import multiply
from app.algorithms.inverse import inverse
from app.algorithms.elimination import rref
from app.results.calculation_step import CalculationStep
from app.exceptions import NonSquareMatrixError, LinearDependenceError, SingularMatrixError
from app.utils.numeric import clean_number, is_zero, is_close, clean_complex, format_number

def eigenvalues(A, max_iterations=1000, record_steps=False):
    steps = [] if record_steps else None
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

        if steps is not None:
            steps.append(
                CalculationStep(
                    description=(
                        "Compute the trace:\n"
                        f"tr(A) = {format_number(a)} + "
                        f"{format_number(d)} = "
                        f"{format_number(trace)}"
                    ), result=None))

            steps.append(
                CalculationStep(
                    description=(
                        "Compute the determinant:\n"
                        f"det(A) = "
                        f"({format_number(a)})"
                        f"({format_number(d)}) - "
                        f"({format_number(b)})"
                        f"({format_number(c)}) = "
                        f"{format_number(det)}"
                    ), result=None))

            steps.append(
                CalculationStep(
                    description=(
                        "Form the characteristic equation:\n"
                        "λ² - tr(A)λ + det(A) = 0\n"
                        f"λ² - {format_number(trace)}λ "
                        f"+ ({format_number(det)}) = 0"
                    ), result=None))

            steps.append(
                CalculationStep(
                    description=(
                        "Compute the discriminant:\n"
                        "Δ = tr(A)² - 4det(A)\n"
                        f"Δ = ({format_number(trace)})² "
                        f"- 4({format_number(det)})\n"
                        f"Δ = {format_number(discriminant)}"
                    ), result=None))

        sqrt_discriminant = cmath.sqrt(discriminant)

        lambda1 = (trace + sqrt_discriminant) / 2
        lambda2 = (trace - sqrt_discriminant) / 2

        values = [clean_complex(lambda1), clean_complex(lambda2),]

        if steps is not None:
            steps.append(
                CalculationStep(
                    description=(
                        "Apply the quadratic formula:\n"
                        f"λ = ({format_number(trace)} ± "
                        f"√{format_number(discriminant)}) / 2"
                    ), result=None))

            steps.append(
                CalculationStep(
                    description=(
                        "Eigenvalues:\n"
                        f"λ₁ = {format_number(values[0])}\n"
                        f"λ₂ = {format_number(values[1])}"
                    ), result=None))

        if record_steps:
            return values, steps
        return values

    # Complex shifted QR also handles zero eigenvalues and conjugate pairs.
    current = A.copy()
    active = A.rows
    iterations = 0
    if steps is not None:
        steps.append(CalculationStep("Start with A; QR similarity transformations preserve its eigenvalues.", A.copy()))

    while active > 1:
        scale = max(abs(current[row][col]) for row in range(active) for col in range(active))
        # Test the entire trailing row because the input need not be Hessenberg.
        if all(abs(current[active - 1][col]) <= 1e-12 * scale for col in range(active - 1)):
            for col in range(active - 1):
                current[active - 1][col] = 0.0
            if steps is not None:
                steps.append(CalculationStep(
                    f"The last row of the active block is triangular. Read eigenvalue "
                    f"{format_number(current[active - 1][active - 1])} and continue with the smaller block.",
                    current.copy()))
            active -= 1
            continue
        if iterations >= max_iterations:
            raise ValueError("Eigenvalue iteration did not converge.")

        a, b = current[active - 2][active - 2], current[active - 2][active - 1]
        c, d = current[active - 1][active - 2], current[active - 1][active - 1]
        root = cmath.sqrt(((a - d) / 2) ** 2 + b * c)
        candidates = [(a + d) / 2 + root, (a + d) / 2 - root]
        shift = min(candidates, key=lambda value: abs(value - d))
        # Break occasional cycles when the trailing block gives a poor shift.
        if iterations and iterations % 20 == 0:
            shift = d + complex(0.75, 0.25) * scale
        shifted = Matrix([
            [current[row][col] - (shift if row == col else 0) for col in range(active)]
            for row in range(active)])
        Q, R = _eigen_qr(shifted)
        next_block = multiply(R, Q)
        # Apply the same similarity transform to columns outside the active block.
        trailing = [
            [sum(complex(Q[k][row]).conjugate() * current[k][col] for k in range(active))
             for col in range(active, A.rows)]
            for row in range(active)]
        for row in range(active):
            for col in range(active):
                current[row][col] = next_block[row][col] + (shift if row == col else 0)
            for col in range(active, A.rows):
                current[row][col] = trailing[row][col - active]
        iterations += 1
        # Keep long calculations readable without building thousands of widgets.
        if steps is not None and (iterations <= 8 or iterations % 25 == 0):
            steps.append(CalculationStep(
                f"QR iteration {iterations}: factor the active block minus "
                f"({format_number(shift)})I into QR. Q is:", Q.copy()))
            steps.append(CalculationStep("The corresponding upper triangular R is:", R.copy()))
            steps.append(CalculationStep(
                f"Compute RQ + ({format_number(shift)})I for the next active block. "
                "After iteration 8, intermediate snapshots are shown every 25 iterations.", current.copy()))

    values = [clean_complex(complex(current[i][i])) for i in range(A.rows)]
    if steps is not None:
        summary = "\n".join(f"Eigenvalue {i + 1} = {format_number(value)}" for i, value in enumerate(values))
        steps.append(CalculationStep("Read the eigenvalues from the diagonal:\n" + summary, current.copy()))
        steps.append(CalculationStep(description="QR iteration converged.", result=current.copy()))
    if record_steps:
        return values, steps
    return values


def _eigen_qr(A):
    """Square complex Householder QR; zero/dependent columns are valid here."""
    n = A.rows
    R = [[complex(value) for value in row] for row in A.data]
    Q = [[complex(row == col) for col in range(n)] for row in range(n)]
    for pivot in range(n):
        vector = [R[row][pivot] for row in range(pivot, n)]
        magnitude = math.hypot(*(abs(value) for value in vector))
        if magnitude == 0:
            continue
        phase = vector[0] / abs(vector[0]) if vector[0] != 0 else 1
        vector = [value / magnitude for value in vector]
        vector[0] += phase
        length = math.hypot(*(abs(value) for value in vector))
        vector = [value / length for value in vector]
        for col in range(pivot, n):
            projection = 2 * sum(value.conjugate() * R[pivot + i][col] for i, value in enumerate(vector))
            for i, value in enumerate(vector):
                R[pivot + i][col] -= value * projection
        for row in range(n):
            projection = 2 * sum(Q[row][pivot + i] * value for i, value in enumerate(vector))
            for i, value in enumerate(vector):
                Q[row][pivot + i] -= projection * value.conjugate()
        for row in range(pivot + 1, n):
            R[row][pivot] = 0j
    return Matrix(Q), Matrix(R)


def eigenvectors(A, record_steps=False):
    if record_steps:
        values, value_steps = eigenvalues(A, record_steps=True)
        steps = value_steps
    else:
        values = eigenvalues(A)
        steps = None
    vectors = []
    processed = []

    for eigenvalue in values:
        already_processed = any(is_close(eigenvalue, processed_value) for processed_value in processed)

        if already_processed:
            continue

        basis = eigenspace_basis(A, eigenvalue)
        vectors.extend(basis)
        processed.append(eigenvalue)

        if steps is not None:
            for vector in basis:
                steps.append(CalculationStep(description=(f"Find eigenvector for " f"λ = {format_number(eigenvalue)}"), result=vector.copy()))

    if record_steps:
        return vectors, steps
    return vectors

def diagonalize(A, record_steps=False):
    if record_steps:
        vectors, steps = eigenvectors(A, record_steps=True)
        values = eigenvalues(A)
    else:
        values = eigenvalues(A)
        vectors = eigenvectors(A)
        steps = None

    if len(vectors) != A.columns:
        raise LinearDependenceError

    P = Matrix([
        [vectors[column][row] for column in range(len(vectors))]
        for row in range(A.rows)])

    if steps is not None:
        steps.append(CalculationStep(description="Build P from the eigenvectors.", result=P.copy()))

    try:
        P_inverse = inverse(P)
    except SingularMatrixError:
        raise LinearDependenceError

    D = Matrix([
        [values[row] if row == column else 0.0
            for column in range(A.columns)]
        for row in range(A.rows)])

    if steps is not None:
        steps.append(CalculationStep(description="Build diagonal matrix D from the eigenvalues.", result=D.copy()))

    if record_steps:
        return P, D, P_inverse, steps
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
