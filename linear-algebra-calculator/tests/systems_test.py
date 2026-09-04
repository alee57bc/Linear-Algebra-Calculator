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

def test_solve_system_integer_solution():
    A = Matrix([
        [1, 1],
        [2, -1]
    ])
    b = Vector([5, 1])
    result = solve_system(A, b)
    expected = [2.0, 3.0]

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

