from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget
from app.core.matrix import Matrix
from app.utils.numeric import clean_number, format_number

class ResultView(QWidget):
    def __init__(self, matrix=None):
        super().__init__()
        self.matrix = matrix
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.title = QLabel("Result")
        self.layout.addWidget(self.title)
        self.matrix_layout = QGridLayout()
        self.layout.addLayout(self.matrix_layout)

        if matrix is not None:
            self.update_matrix(matrix)

    def update_matrix(self, matrix):
        self.matrix = matrix

        # Remove the old result cells
        while self.matrix_layout.count():
            item = self.matrix_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add the new matrix values
        for row in range(matrix.rows):
            for column in range(matrix.columns):
                cleaned = clean_number(matrix[row][column])
                value = QLabel(format_number(matrix[row][column]))
                self.matrix_layout.addWidget(value, row, column)