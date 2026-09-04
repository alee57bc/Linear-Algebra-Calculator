from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import transpose, multiply, matrix_vector_multiply
from app.algorithms.systems import solve_system
from app.results.system_solution import SolutionType
from app.exceptions import DimensionMismatchError, LinearDependenceError

def least_squares(A, b):
    if A.rows != b.dimension:
        raise DimensionMismatchError

    A_transpose = transpose(A)
    normal_matrix = multiply(A_transpose, A)
    normal_vector = matrix_vector_multiply(A_transpose, b)
    result = solve_system(normal_matrix, normal_vector)

    if result.solution_type != SolutionType.UNIQUE:
        raise LinearDependenceError
    return result.solution