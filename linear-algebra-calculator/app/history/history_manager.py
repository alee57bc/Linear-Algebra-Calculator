from app.core.matrix import Matrix
from app.core.vector import Vector
from app.history.history_entry import HistoryEntry

class HistoryManager:
    def __init__(self):
        self._entries = []

    @property
    def entries(self):
        return self._entries.copy()

    def add_entry(self, operation, inputs, result):
        stored_inputs = []

        for value in inputs:
            if isinstance(value, (Matrix, Vector)):
                stored_inputs.append(value.copy())
            else:
                stored_inputs.append(value)

        if isinstance(result, (Matrix, Vector)):
            stored_result = result.copy()
        else:
            stored_result = result

        entry = HistoryEntry(operation=operation, inputs=stored_inputs, result=stored_result)
        self._entries.append(entry)

    def clear(self):
        self._entries.clear()

    def get_entry(self, index):
        return self._entries[index]

    def __len__(self):
        return len(self._entries)