from app.core.matrix import Matrix
from app.core.vector import Vector
from app.algorithms.elimination import rref
from app.utils.numeric import is_zero, is_close
from app.results.system_solution import SystemSolution, SolutionType
from app.utils.cleanup import clean_vector

def solve_system(A: Matrix, b: Vector):
    if A.rows != b.dimension:
        raise ValueError(
            "The number of rows in A must match the dimension of b."
        )

    augmented_data = [
            A[i][:] + [b[i]]
            for i in range(A.rows)]

    augmented = Matrix(augmented_data)
    reduced = rref(augmented)

    # Check for inconsistent rows
    for row in range(reduced.rows):
        coefficients_are_zero = all(
                    is_zero(reduced[row][column])
                    for column in range(A.columns))

        constant = reduced[row][A.columns]

        if coefficients_are_zero and not is_zero(constant):
            return SystemSolution(
                solution_type=SolutionType.NO_SOLUTION
            )

    # Check whether there is a unique solution
    pivot_count = 0

    for row in range(reduced.rows):
        for column in range(A.columns):
            if not is_zero(reduced[row][column]):
                pivot_count += 1
                break

    if pivot_count < A.columns:
        return SystemSolution(solution_type=SolutionType.INFINITE)

    solution = Vector([
        reduced[row][A.columns]
        for row in range(A.columns)])

    return SystemSolution(
        solution_type=SolutionType.UNIQUE,
        solution=clean_vector(solution))