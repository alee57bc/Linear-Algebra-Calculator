from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QGridLayout, QLabel, QLayout, QScrollArea, QVBoxLayout, QWidget
from app.core.matrix import Matrix
from app.utils.numeric import format_number

class ResultView(QWidget):
    def __init__(self, matrix=None):
        super().__init__()
        self.matrix = matrix
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setSizeConstraint(QLayout.SetMinimumSize)
        content_layout.setContentsMargins(20, 16, 20, 16)
        self.empty_label = QLabel("No result yet")
        self.empty_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.empty_label)
        self.matrix_layout = QGridLayout()
        self.matrix_layout.setHorizontalSpacing(24)
        self.matrix_layout.setVerticalSpacing(12)
        self.matrix_layout.setAlignment(Qt.AlignCenter)
        content_layout.addLayout(self.matrix_layout)
        self.content_widget.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        if matrix is not None:
            self.update_matrix(matrix)

    def clear_result(self):
        self.matrix = None
        self.empty_label.show()
        for row in range(self.matrix_layout.rowCount()):
            self.matrix_layout.setRowMinimumHeight(row, 0)
        for column in range(self.matrix_layout.columnCount()):
            self.matrix_layout.setColumnMinimumWidth(column, 0)
        while self.matrix_layout.count():
            item = self.matrix_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    def update_scalar(self, value):
        self.clear_result()
        self.empty_label.hide()
        label = QLabel(format_number(value))
        self.matrix_layout.addWidget(label, 0, 0)

    def update_matrix(self, matrix):
        self.clear_result()
        self.empty_label.hide()
        self.matrix = matrix
        for row in range(matrix.rows):
            for column in range(matrix.columns):
                value = QLabel(format_number(matrix[row][column]))
                self.matrix_layout.addWidget(value, row, column)

    def update_matrices(self, matrices):
        self.clear_result()
        self.empty_label.setVisible(not matrices)
        column_offset = 0

        for name, matrix in matrices:
            if column_offset:
                self.matrix_layout.setColumnMinimumWidth(column_offset - 1, 28)
            title = QLabel(f"{name} =")
            title.setAlignment(Qt.AlignCenter)
            self.matrix_layout.addWidget(title, 0, column_offset, 1, matrix.columns)

            for row in range(matrix.rows):
                for column in range(matrix.columns):
                    value = QLabel(format_number(matrix[row][column]))
                    value.setAlignment(Qt.AlignCenter)
                    self.matrix_layout.addWidget(value, row + 1, column_offset + column)

            column_offset += matrix.columns + 1

    def update_values(self, values):
        self.clear_result()
        self.empty_label.setVisible(not values)

        for index, value in enumerate(values):
            subscript = str(index + 1).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            label = QLabel(f"λ{subscript} = {format_number(value)}")
            self.matrix_layout.addWidget(label, index, 0)

    def update_vectors(self, vectors):
        self.clear_result()
        self.empty_label.setVisible(not vectors)

        for index, vector in enumerate(vectors):
            text = "[" + "  ".join(format_number(value) for value in vector.data) + "]"
            subscript = str(index + 1).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            label = QLabel(f"v{subscript} = {text}")
            self.matrix_layout.addWidget(label, index, 0)
