from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QWidget
from app.core.matrix import Matrix
from app.ui.matrix_editor import MatrixEditor
from app.ui.result_view import ResultView
from app.core.basic_operations import add, subtract, scalar_multiply, multiply, transpose

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Algebra Calculator")
        self.result_view = ResultView()

    #------ Matrix A ------
        self.rows_a = 2
        self.columns_a = 2
        self.matrix_a = Matrix([
            [0, 0],
            [0, 0]
        ])
        self.matrix_a_editor = MatrixEditor(self.matrix_a)

        #set up row and column spinbox for matrix a
        self.rows_a_spinbox = QSpinBox()
        self.rows_a_spinbox.setRange(1, 10)
        self.rows_a_spinbox.setValue(self.rows_a)
        self.columns_a_spinbox = QSpinBox()
        self.columns_a_spinbox.setRange(1, 10)
        self.columns_a_spinbox.setValue(self.columns_a)

        #set up row and column spinbox layout in UI for matrix a
        rows_a_layout = QHBoxLayout()
        rows_a_layout.addWidget(QLabel("Rows:"))
        rows_a_layout.addWidget(self.rows_a_spinbox)
        columns_a_layout = QHBoxLayout()
        columns_a_layout.addWidget(QLabel("Columns:"))
        columns_a_layout.addWidget(self.columns_a_spinbox)

        #set up matrix a in UI
        matrix_a_layout = QHBoxLayout()
        matrix_a_layout.addLayout(rows_a_layout)
        matrix_a_layout.addLayout(columns_a_layout)

        #set up read matrix a button
        self.read_matrix_a_button = QPushButton("Get Matrix A")
        self.read_matrix_a_button.clicked.connect(self.print_matrix_a)

    #------ Matrix B ------
        self.rows_b = 2
        self.columns_b = 2
        self.matrix_b = Matrix([
            [0, 0],
            [0, 0]
        ])
        self.matrix_b_editor = MatrixEditor(self.matrix_b)
        self.matrix_b_widget = QWidget()

        #set up row and column spinbox for matrix b
        self.rows_b_spinbox = QSpinBox()
        self.rows_b_spinbox.setRange(1, 10)
        self.rows_b_spinbox.setValue(self.rows_b)
        self.columns_b_spinbox = QSpinBox()
        self.columns_b_spinbox.setRange(1, 10)
        self.columns_b_spinbox.setValue(self.columns_b)

        #set up row and column spinbox layout in UI for matrix b
        rows_b_layout = QHBoxLayout()
        rows_b_layout.addWidget(QLabel("Rows:"))
        rows_b_layout.addWidget(self.rows_b_spinbox)
        columns_b_layout = QHBoxLayout()
        columns_b_layout.addWidget(QLabel("Columns:"))
        columns_b_layout.addWidget(self.columns_b_spinbox)

        #set up matrix b in UI
        matrix_b_layout = QHBoxLayout()
        matrix_b_layout.addLayout(rows_b_layout)
        matrix_b_layout.addLayout(columns_b_layout)

        #set up read matrix b button
        self.read_matrix_b_button = QPushButton("Get Matrix B")
        self.read_matrix_b_button.clicked.connect(self.print_matrix_b)

        #set up matrix b widget visibility
        matrix_b_widget_layout = QVBoxLayout()
        matrix_b_widget_layout.addWidget(QLabel("Matrix B"))
        matrix_b_widget_layout.addLayout(matrix_b_layout)
        matrix_b_widget_layout.addWidget(self.matrix_b_editor)
        matrix_b_widget_layout.addWidget(self.read_matrix_b_button)
        self.matrix_b_widget.setLayout(matrix_b_widget_layout)

    #------ Operations ------
        self.operation_selector = QComboBox()
        self.operation_selector.addItems([
              "Addition",
              "Subtraction",
              "Scalar Multiplication",
              "Matrix Multiplication",
              "Transpose",
        ])
        #add operation layout
        operation_layout = QHBoxLayout()
        operation_layout.addWidget(QLabel("Operation:"))
        operation_layout.addWidget(self.operation_selector)

        #dynamic operations
        self.operation_selector.currentTextChanged.connect(
            self.update_operation_ui
        )

        #scalar input
        self.scalar_input = QLineEdit()
        self.scalar_input.setPlaceholderText("Enter scalar")
        self.scalar_input.setText("1.0")

        #scalar layout
        scalar_layout = QHBoxLayout()
        scalar_layout.addWidget(QLabel("Scalar:"))
        scalar_layout.addWidget(self.scalar_input)
        self.scalar_widget = QWidget()
        self.scalar_widget.setLayout(scalar_layout)
        self.scalar_widget.setVisible(False)

        #calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

    #------ Main layout ------
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Matrix A"))
        layout.addLayout(matrix_a_layout)
        layout.addWidget(self.matrix_a_editor)
        layout.addWidget(self.read_matrix_a_button)

        layout.addLayout(operation_layout)
        layout.addWidget(self.scalar_widget)

        layout.addWidget(self.matrix_b_widget)

        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_view)

    #------ Central Widget ------
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    #------ Dimensions ------
        self.rows_a_spinbox.valueChanged.connect(self.change_a_dimensions)
        self.columns_a_spinbox.valueChanged.connect(self.change_a_dimensions)

        self.rows_b_spinbox.valueChanged.connect(self.change_b_dimensions)
        self.columns_b_spinbox.valueChanged.connect(self.change_b_dimensions)

    #------ Scalar Text ------
        scalar_text = self.scalar_input.text()
        scalar = float(scalar_text)

    def change_a_dimensions(self):
        rows = self.rows_a_spinbox.value()
        columns = self.columns_a_spinbox.value()
        old_matrix = self.matrix_a_editor.get_matrix()
        data = []

        #keep old data when adding new row or column
        for row in range(rows):
            row_data = []
            for column in range(columns):
                if row < old_matrix.rows and column < old_matrix.columns:
                    row_data.append(old_matrix[row][column])
                else:
                    row_data.append(0.0)
            data.append(row_data)
        self.matrix_a = Matrix(data)
        self.matrix_a_editor.update_matrix(self.matrix_a)

    def change_b_dimensions(self):
        rows = self.rows_b_spinbox.value()
        columns = self.columns_b_spinbox.value()
        old_matrix = self.matrix_b_editor.get_matrix()
        data = []

        #keep old data when adding new row or column
        for row in range(rows):
            row_data = []
            for column in range(columns):
                if row < old_matrix.rows and column < old_matrix.columns:
                    row_data.append(old_matrix[row][column])
                else:
                    row_data.append(0.0)
            data.append(row_data)
        self.matrix_b = Matrix(data)
        self.matrix_b_editor.update_matrix(self.matrix_b)

    def print_matrix_a(self):
        matrix = self.matrix_a_editor.get_matrix()
        if matrix is None:
                return
        print("Matrix A:")
        print(matrix)

    def print_matrix_b(self):
        matrix = self.matrix_b_editor.get_matrix()
        if matrix is None:
                return
        print("Matrix B:")
        print(matrix)

    def update_operation_ui(self):
        operation = self.operation_selector.currentText()

        needs_matrix_b = operation in [
            "Addition",
            "Subtraction",
            "Matrix Multiplication"
        ]
        self.matrix_b_widget.setVisible(needs_matrix_b)

        needs_scalar = operation == "Scalar Multiplication"
        self.scalar_widget.setVisible(needs_scalar)

    def calculate(self):
        operation = self.operation_selector.currentText()
        matrix_a = self.matrix_a_editor.get_matrix()

        try:
            if operation == "Addition":
                matrix_b = self.matrix_b_editor.get_matrix()
                result = add(matrix_a, matrix_b)
            elif operation == "Subtraction":
                matrix_b = self.matrix_b_editor.get_matrix()
                result = subtract(matrix_a, matrix_b)
            elif operation == "Scalar Multiplication":
                scalar = float(self.scalar_input.text())
                result = scalar_multiply(matrix_a, scalar)
            elif operation == "Matrix Multiplication":
                matrix_b = self.matrix_b_editor.get_matrix()
                result = multiply(matrix_a, matrix_b)
            elif operation == "Transpose":
                result = transpose(matrix_a)
            else:
                return
            self.result_view.update_matrix(result)

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Invalid Operation",
                str(error)
            )

