from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from app.core.matrix import Matrix

class MatrixEditor(QTableWidget):
    def __init__(self, matrix, parent=None):
        super().__init__(parent)
        self.matrix = matrix
        self.update_matrix(matrix)

    def update_matrix(self, matrix):
        self.matrix = matrix
        self.setRowCount(matrix.rows)
        self.setColumnCount(matrix.columns)
        self.clearContents()
        for row in range(matrix.rows):
            for column in range(matrix.columns):
                value = matrix[row][column]
                item = QTableWidgetItem(str(value))
                self.setItem(row, column, item)

    def get_matrix(self):
        data = []
        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is None:
                    value = 0.0
                else:
                    text = item.text().strip()
                    try:
                         value = float(text)
                    except ValueError:
                         QMessageBox.warning(
                             self,
                             "Invalid Matrix Value",
                             f"Invalid value in row {row + 1}, "
                             f"column {column + 1}."
                         )
                         return None
                row_data.append(value)
            data.append(row_data)
        return Matrix(data)