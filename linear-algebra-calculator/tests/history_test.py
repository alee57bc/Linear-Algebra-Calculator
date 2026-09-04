from app.core.matrix import Matrix
from app.history.history_manager import HistoryManager

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