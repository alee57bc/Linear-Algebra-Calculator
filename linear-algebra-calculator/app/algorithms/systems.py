from app.core.matrix import Matrix
from app.core.vector import Vector
from app.algorithms.elimination import rref
from app.utils.numeric import is_zero, is_close

def solve_system(A: Matrix, b: Vector):
    if A.rows != b.dimension:
        raise ValueError(
            "The number of rows in A must match the dimension of b."
        )
    augmented_data = []

    for i in range(A.rows):
        augmented_data.append(
            A[i][:] + [b[i]]
        )

    augmented = Matrix(augmented_data)
    reduced = rref(augmented)

    # Check for inconsistent rows
    for row in range(reduced.rows):
        all_zero = all(
            is_zero(reduced[row][column])
            for column in range(A.columns)
        )
        last_value = reduced[row][A.columns]

        if all_zero and not is_zero(last_value):
            raise ValueError("System has no solution.")

    # Check whether there is a unique solution
    pivot_count = 0

    for row in range(reduced.rows):
        for column in range(A.columns):
            if is_close(reduced[row][column], 1.0):
                pivot = True
                for other_column in range(A.columns):
                    if other_column != column:
                        if not is_zero(reduced[row][other_column]):
                            pivot = False
                            break
                if pivot:
                    pivot_count += 1
                break

    if pivot_count < A.columns:
        raise ValueError(
            "System has infinitely many solutions."
        )

    solution = [
        reduced[i][A.columns]
        for i in range(A.columns)
    ]

    return Vector(solution)