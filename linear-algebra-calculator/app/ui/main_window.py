from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget
from app.core.matrix import Matrix
from app.ui.matrix_editor import MatrixEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Algebra Calculator")
        self.rows = 2
        self.columns = 3
        self.matrix = Matrix([
            [0, 0, 0],
            [0, 0, 0]
        ])
        self.matrix_editor = MatrixEditor(self.matrix)

        #set up row and column spinbox
        self.rows_spinbox = QSpinBox()
        self.rows_spinbox.setRange(1, 10)
        self.rows_spinbox.setValue(self.rows)
        self.columns_spinbox = QSpinBox()
        self.columns_spinbox.setRange(1, 10)
        self.columns_spinbox.setValue(self.columns)

        #set up row and column spinbox layout in GUI
        rows_layout = QHBoxLayout()
        rows_layout.addWidget(QLabel("Rows:"))
        rows_layout.addWidget(self.rows_spinbox)
        columns_layout = QHBoxLayout()
        columns_layout.addWidget(QLabel("Columns:"))
        columns_layout.addWidget(self.columns_spinbox)

        #set up matrix in GUI
        controls_layout = QHBoxLayout()
        controls_layout.addLayout(rows_layout)
        controls_layout.addLayout(columns_layout)

        #set up read matrix to print matrix to terminal
        self.read_matrix_button = QPushButton("Get Matrix")
        self.read_matrix_button.clicked.connect(self.print_matrix)

        #layout for main matrix page
        layout = QVBoxLayout()
        layout.addLayout(controls_layout)
        layout.addWidget(self.matrix_editor)
        layout.addWidget(self.read_matrix_button)
        layout.addWidget(self.load_matrix_button)

        #put UI pieces into main window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        #auto update matrix
        self.rows_spinbox.valueChanged.connect(self.change_dimensions)
        self.columns_spinbox.valueChanged.connect(self.change_dimensions)

    def change_dimensions(self):
        self.rows = self.rows_spinbox.value()
        self.columns = self.columns_spinbox.value()
        old_matrix = self.matrix_editor.get_matrix()
        data = []

        #keep old data when adding new row or column
        for row in range(self.rows):
            row_data = []
            for column in range(self.columns):
                if row < old_matrix.rows and column < old_matrix.columns:
                    row_data.append(old_matrix[row][column])
                else:
                    row_data.append(0.0)
            data.append(row_data)
        self.matrix = Matrix(data)
        self.matrix_editor.update_matrix(self.matrix)

    def print_matrix(self):
        matrix = self.matrix_editor.get_matrix()
        if matrix is None:
                return
        print("Matrix from UI:")
        print(matrix)