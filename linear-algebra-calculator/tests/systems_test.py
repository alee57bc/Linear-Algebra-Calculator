import pytest
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.algorithms.systems import solve_system
from app.results.system_solution import SolutionType

def test_solve_system():
    A = Matrix([
        [2, 1],
        [1, 3]
    ])
    b = Vector([5, 6])
    result = solve_system(A, b)
    expected = [1.8, 1.4]

    assert result.solution_type == SolutionType.UNIQUE
    assert result.solution.data == pytest.approx(expected)

def test_solve_system_integer_solution():
    A = Matrix([
        [1, 1],
        [2, -1]
    ])
    b = Vector([5, 1])
    result = solve_system(A, b)
    expected = [2.0, 3.0]

    assert result.solution_type == SolutionType.UNIQUE
    assert result.solution.data == pytest.approx(expected)


def test_solve_system_dimension_mismatch():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])
    b = Vector([1, 2, 3])

    with pytest.raises(ValueError):
        solve_system(A, b)

def test_no_solution():
    A = Matrix([
        [1, 1],
        [2, 2]
    ])
    b = Vector([
        2,
        5
    ])

    result = solve_system(A, b)
    assert result.solution_type == SolutionType.NO_SOLUTION
    assert result.solution is None

def test_infinitely_many_solutions():
    A = Matrix([
        [1, 1],
        [2, 2]
    ])
    b = Vector([
        2,
        4
    ])

    result = solve_system(A, b)
    assert result.solution_type == SolutionType.INFINITE
    assert result.solution is None


@pytest.mark.parametrize("data, constants, solution_type, expected", [
    ([[1, 0], [0, 1], [1, 1]], [2, 3, 5], SolutionType.UNIQUE, [2, 3]),
    ([[1, 0], [0, 1], [1, 1]], [2, 3, 6], SolutionType.NO_SOLUTION, None),
    ([[1, 1, 1]], [2], SolutionType.INFINITE, None),
    ([[0, 0], [0, 0]], [0, 0], SolutionType.INFINITE, None),
])
def test_rectangular_and_zero_systems(data, constants, solution_type, expected):
    matrix, vector = Matrix(data), Vector(constants)
    result = solve_system(matrix, vector)
    assert result.solution_type == solution_type
    if expected is None:
        assert result.solution is None
    else:
        assert result.solution.data == pytest.approx(expected)
    assert matrix.data == data
    assert vector.data == constants

