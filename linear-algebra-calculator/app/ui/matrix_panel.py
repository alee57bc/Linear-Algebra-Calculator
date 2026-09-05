from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout
from app.core.matrix import Matrix
from app.ui.matrix_editor import MatrixEditor

class MatrixPanel(QGroupBox):
    input_changed = Signal()

    def __init__(self, title):
        super().__init__(title)
        self.base_title = title
        self.setMinimumSize(280, 210)
        self.matrix = Matrix([[0, 0], [0, 0]])
        self.rows = 2
        self.columns = 2
        self.editor = MatrixEditor(self.matrix)

        self.rows_spinbox = QSpinBox()
        self.rows_spinbox.setRange(1, 10)
        self.rows_spinbox.setValue(self.rows)

        self.columns_spinbox = QSpinBox()
        self.columns_spinbox.setRange(1, 10)
        self.columns_spinbox.setValue(self.columns)

        for spinbox in (self.rows_spinbox, self.columns_spinbox):
            spinbox.setMinimumSize(80, 32)

        dimensions_layout = QHBoxLayout()

        dimensions_layout.addWidget(QLabel("Rows:"))
        dimensions_layout.addWidget(self.rows_spinbox)

        dimensions_layout.addWidget(QLabel("Columns:"))
        dimensions_layout.addWidget(self.columns_spinbox)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 20, 14, 14)
        layout.setSpacing(10)
        layout.addLayout(dimensions_layout)
        layout.addWidget(self.editor)

        self.setLayout(layout)

        self.rows_spinbox.valueChanged.connect(self.change_dimensions)
        self.columns_spinbox.valueChanged.connect(self.change_dimensions)
        self.editor.itemChanged.connect(lambda _item: self.input_changed.emit())
        self.setTitle(f"{self.base_title} (2 × 2)")

    def get_matrix(self):
        return self.editor.get_matrix()

    def set_matrix(self, matrix):
        self.matrix = matrix

        self.rows_spinbox.blockSignals(True)
        self.columns_spinbox.blockSignals(True)

        self.rows_spinbox.setValue(matrix.rows)
        self.columns_spinbox.setValue(matrix.columns)

        self.rows_spinbox.blockSignals(False)
        self.columns_spinbox.blockSignals(False)

        self.editor.update_matrix(matrix)
        self.rows, self.columns = matrix.rows, matrix.columns
        self.setTitle(f"{self.base_title} ({matrix.rows} × {matrix.columns})")
        self.input_changed.emit()

    def change_dimensions(self):
        old_matrix = self.editor.get_matrix()

        if old_matrix is None:
            return

        rows = self.rows_spinbox.value()
        columns = self.columns_spinbox.value()
        data = []

        for row in range(rows):
            row_data = []
            for column in range(columns):
                if (row < old_matrix.rows and column < old_matrix.columns):
                    row_data.append(old_matrix[row][column])
                else:
                    row_data.append(0.0)

            data.append(row_data)
        self.set_matrix(Matrix(data))
