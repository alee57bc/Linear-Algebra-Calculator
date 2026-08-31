#handle construction, dimensions, access, and modification

class Matrix:

     def __init__(self, data):
         self._data = [
            [float(value) for value in row]
            for row in data
         ]

     @property
     def data(self):
         return self._data

     @property
     def rows(self):
         return len(self._data)

     @property
     def columns(self):
         if self._data:
            return len(self._data[0])
         else:
             return 0

     def __getitem__(self, index):
         return self._data[index]

     def __setitem__(self, index, value):
         self._data[index] = value

     def __str__(self):
        return "\n".join(
                    "[" + " ".join(map(str, row)) + "]"
                    for row in self._data
                )
