from app.utils.numeric import to_numeric

class Matrix:
     def __init__(self, data):
         #check inputs
         if not isinstance(data, list):
             raise TypeError("Matrix data must be a list of rows.")

         if len(data) == 0:
             raise ValueError("Matrix cannot be empty.")

         if not all(isinstance(row, list) for row in data):
             raise TypeError("Each matrix row must be a list.")

         if len(data[0]) == 0:
             raise ValueError("Matrix rows cannot be empty.")

         column_count = len(data[0])

         for row in data:
             if len(row) != column_count:
                 raise ValueError("All matrix rows must have the same length.")
         try:
             self._data = [[to_numeric(value) for value in row] for row in data]
         except (TypeError, ValueError):
             raise ValueError("Matrix values must be numeric.")

     def __eq__(self, other):
         if not isinstance(other, Matrix):
             return False
         return self._data == other._data

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
         self._data[index] = [to_numeric(item) for item in value]

     def copy(self):
         return Matrix([row[:] for row in self._data])

     def __str__(self):
        return "\n".join(
                    "[" + " ".join(map(str, row)) + "]"
                    for row in self._data
                )
