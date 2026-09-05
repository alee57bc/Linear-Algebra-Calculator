from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import transpose, multiply, matrix_vector_multiply
from app.algorithms.systems import solve_system
from app.algorithms.decompositions import qr_decomposition
from app.results.system_solution import SolutionType
from app.exceptions import DimensionMismatchError, LinearDependenceError

def least_squares(A, b):
    if A.rows != b.dimension:
        raise DimensionMismatchError

    Q, R = qr_decomposition(A)
    Q_transpose = transpose(Q)

    transformed_b = matrix_vector_multiply(Q_transpose, b)
    result = solve_system(R, transformed_b)

    if result.solution_type != SolutionType.UNIQUE:
        raise LinearDependenceError

    return result.solution