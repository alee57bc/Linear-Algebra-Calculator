from app.core.matrix import Matrix
from app.history.history_manager import HistoryManager
from app.core.vector import Vector
from app.results.calculation_step import CalculationStep

def test_history_starts_empty():
    history = HistoryManager()

    assert history.entries == []

def test_add_history_entry():
    history = HistoryManager()
    A = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = Matrix([
        [2, 4],
        [6, 8]
    ])
    history.add_entry("Scalar Multiplication", [A, 2], result)

    assert len(history.entries) == 1
    assert history.entries[0].operation == "Scalar Multiplication"

def test_history_stores_result():
    history = HistoryManager()
    A = Matrix([
        [1, 2],
        [3, 4]
    ])
    result = Matrix([
        [2, 3],
        [4, 5]
    ])
    history.add_entry("Addition", [A, A], result)

    assert history.entries[0].result == result

def test_clear_history():
    history = HistoryManager()
    A = Matrix([
        [1]
    ])
    history.add_entry("Transpose", [A], A)
    history.clear()

    assert history.entries == []


def test_history_copies_inputs_results_and_extra_matrices():
    history = HistoryManager()
    matrix, vector = Matrix([[2]]), Vector([3])
    steps = [CalculationStep("Original", matrix.copy())]
    extras = [("A", matrix)]
    history.add_entry("Example", [matrix, vector, 2], vector, steps, extras)
    matrix[0][0] = 99
    vector[0] = 99
    steps.clear()
    extras.clear()
    entry = history.get_entry(0)
    assert entry.inputs[0] == Matrix([[2]])
    assert entry.inputs[1].data == [3]
    assert entry.inputs[2] == 2
    assert entry.result.data == [3]
    assert len(entry.steps) == 1
    assert entry.extra_results == [("A", Matrix([[2]]))]
    history.entries.clear()
    assert len(history) == 1


def test_history_scalar_results_and_order():
    history = HistoryManager()
    history.add_entry("Determinant", [Matrix([[2]])], 2)
    history.add_entry("Determinant", [Matrix([[3]])], 3)
    assert [entry.result for entry in history.entries] == [2, 3]
    assert history.get_entry(0).steps == []
    assert history.get_entry(0).extra_results == []
