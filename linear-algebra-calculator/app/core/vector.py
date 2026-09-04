class Vector:
    def __init__(self, data):
        self._data = [float(value) for value in data]

    @property
    def data(self):
        return self._data

    @property
    def dimension(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = float(value)

    def __str__(self):
        return "[" + " ".join(map(str, self._data)) + "]"