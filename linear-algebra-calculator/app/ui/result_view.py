from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget
from app.core.matrix import Matrix
from app.utils.numeric import clean_number, format_number

class ResultView(QWidget):
    def __init__(self, matrix=None):
        super().__init__()
        self.matrix = matrix
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.matrix_layout = QGridLayout()
        self.layout.addLayout(self.matrix_layout)

        if matrix is not None:
            self.update_matrix(matrix)

    def clear_result(self):
        while self.matrix_layout.count():
            item = self.matrix_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    def update_scalar(self, value):
        self.clear_result()
        label = QLabel(format_number(value))
        self.matrix_layout.addWidget(label, 0, 0)

    def update_matrix(self, matrix):
        self.clear_result()
        for row in range(matrix.rows):
            for column in range(matrix.columns):
                value = QLabel(format_number(matrix[row][column]))
                self.matrix_layout.addWidget(value, row, column)

    def update_matrices(self, matrices):
        self.clear_result()
        current_row = 0

        for label, matrix in matrices:
            title = QLabel(label)
            self.matrix_layout.addWidget(title, current_row, 0, 1, matrix.columns)
            current_row += 1
            for row in range(matrix.rows):
                for column in range(matrix.columns):
                    value = QLabel(format_number(matrix[row][column]))
                    self.matrix_layout.addWidget(value, current_row + row, column)
            current_row += matrix.rows + 1

    def update_values(self, values):
        self.clear_result()

        for index, value in enumerate(values):
            label = QLabel(f"λ{index + 1} = {format_number(value)}")
            self.matrix_layout.addWidget(label, index, 0)

    def update_vectors(self, vectors):
        self.clear_result()

        for index, vector in enumerate(vectors):
            text = "[" + "  ".join(format_number(value) for value in vector.data) + "]"
            label = QLabel(f"v{index + 1} = {text}")
            self.matrix_layout.addWidget(label, index, 0)