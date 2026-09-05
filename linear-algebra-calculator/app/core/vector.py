class Vector:
    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("Vector data must be a list.")

        if len(data) == 0:
            raise ValueError("Vector cannot be empty.")

        try:
            self._data = [
                float(value)
                for value in data
            ]
        except (TypeError, ValueError):
            raise ValueError(
                "Vector values must be numeric."
            )
        self._data = [float(value) for value in data]

    @property
    def data(self):
        return self._data

    @property
    def dimension(self):
        return len(self._data)

    def copy(self):
        return Vector(self._data.copy())

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = float(value)

    def __str__(self):
        return "[" + " ".join(map(str, self._data)) + "]"