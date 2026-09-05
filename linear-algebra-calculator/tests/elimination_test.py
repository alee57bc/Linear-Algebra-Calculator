import pytest
from app.core.matrix import Matrix
from app.algorithms.elimination import swap_rows, scale_row, add_multiple_of_row, gaussian_elimination, rref, rank

def test_swap_rows():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    swap_rows(matrix, 0, 1)

    assert matrix.data == [
        [3.0, 4.0],
        [1.0, 2.0]
    ]

def test_swap_row_with_itself():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    swap_rows(matrix, 0, 0)

    assert matrix.data == [
        [1.0, 2.0],
        [3.0, 4.0]
    ]

def test_scale_row():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    scale_row(matrix, 0, 2)

    assert matrix.data == [
        [2.0, 4.0],
        [3.0, 4.0]
    ]
def test_scale_row_by_zero():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    scale_row(matrix, 0, 0)

    assert matrix.data == [
        [0.0, 0.0],
        [3.0, 4.0]
    ]

def test_add_multiple_of_row():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    add_multiple_of_row(matrix, 0, 1, -3)

    assert matrix.data == [
        [1.0, 2.0],
        [0.0, -2.0]
    ]

def test_gaussian_elimination():
    matrix = Matrix([
        [2, 4, 6],
        [1, 3, 5],
        [3, 7, 9]
    ])
    result = gaussian_elimination(matrix)

    expected = [
        [2.0, 4.0, 6.0],
        [0.0, 1.0, 2.0],
        [0.0, 0.0, -2.0]
    ]

    for actual_row, expected_row in zip(result.data, expected):
        assert actual_row == pytest.approx(expected_row)

def test_gaussian_elimination_swaps_rows():
    matrix = Matrix([
        [0, 2],
        [1, 3]
    ])
    result = gaussian_elimination(matrix)
    expected = [
        [1.0, 3.0],
        [0.0, 2.0]
    ]

    for actual_row, expected_row in zip(result.data, expected):
        assert actual_row == pytest.approx(expected_row)

def test_rref():
    matrix = Matrix([
        [2, 4, 6],
        [1, 3, 5],
        [3, 7, 9]
    ])
    result = rref(matrix)
    expected = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]

    for actual_row, expected_row in zip(result.data, expected):
        assert actual_row == pytest.approx(expected_row)

def test_rref_dependent_rows():
    matrix = Matrix([
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9]
    ])
    result = rref(matrix)
    expected = [
        [1.0, 2.0, 3.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ]

    for actual_row, expected_row in zip(result.data, expected):
        assert actual_row == pytest.approx(expected_row)

def test_rref_rectangular():
    matrix = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])
    result = rref(matrix)
    expected = [
        [1.0, 0.0, -1.0],
        [0.0, 1.0, 2.0]
    ]

    for actual_row, expected_row in zip(result.data, expected):
        assert actual_row == pytest.approx(expected_row)

def test_rref_does_not_modify_original():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    original = [
        [1.0, 2.0],
        [3.0, 4.0]
    ]
    rref(matrix)

    assert matrix.data == original

def test_rank_full_rank():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])

    assert rank(matrix) == 2

def test_rank_one():
    matrix = Matrix([
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9]
    ])

    assert rank(matrix) == 1

def test_rank_two():
    matrix = Matrix([
        [1, 2, 3],
        [2, 4, 6],
        [1, 1, 1]
    ])

    assert rank(matrix) == 2

def test_rank_rectangular():
    matrix = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    assert rank(matrix) == 2

def test_gaussian_elimination_records_steps():
    matrix = Matrix([
        [1, 2],
        [2, 5]
    ])
    result, steps = gaussian_elimination(
        matrix,
        record_steps=True
    )

    assert len(steps) > 0
    assert steps[0].description
    assert isinstance(steps[0].result, Matrix)

def test_rref_records_steps():
    matrix = Matrix([
        [2, 4],
        [1, 3]
    ])
    result, steps = rref(
        matrix,
        record_steps=True
    )

    assert len(steps) > 0
    assert steps[0].description
    assert isinstance(steps[0].result, Matrix)

def test_rref_without_recording_returns_matrix():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = rref(matrix)

    assert isinstance(result, Matrix)

def test_gaussian_without_recording_returns_matrix():
    matrix = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = gaussian_elimination(matrix)

    assert isinstance(result, Matrix)

def test_recorded_steps_are_independent_snapshots():
    matrix = Matrix([
        [2, 4],
        [1, 3]
    ])
    result, steps = rref(
        matrix,
        record_steps=True
    )

    assert len(steps) >= 2
    assert steps[0].result is not steps[1].result

def test_recorded_steps_do_not_modify_original():
    matrix = Matrix([
        [2, 4],
        [1, 3]
    ])
    original = [
        [2.0, 4.0],
        [1.0, 3.0]
    ]

    rref(matrix, record_steps=True)

    assert matrix.data == original

def test_rref_records_row_swap():
    matrix = Matrix([
        [0, 1],
        [1, 2]
    ])
    result, steps = rref(
        matrix,
        record_steps=True
    )

    assert steps[0].description == "R1 ↔ R2"

def test_recorded_snapshot_keeps_original_state():
    matrix = Matrix([
        [2, 4],
        [1, 3]
    ])
    result, steps = rref(
        matrix,
        record_steps=True
    )
    first_snapshot = [
        row.copy()
        for row in steps[0].result.data
    ]

    assert steps[0].result.data == first_snapshot