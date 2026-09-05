import os
from PySide6.QtWidgets import QApplication, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QWidget
from PySide6.QtGui import  QKeySequence, QShortcut
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.ui.matrix_editor import MatrixEditor
from app.ui.result_view import ResultView
from app.ui.step_view import StepView
from app.core.basic_operations import add, subtract, scalar_multiply, multiply, transpose
from app.algorithms.elimination import gaussian_elimination, rref
from app.algorithms.determinant import determinant
from app.algorithms.inverse import inverse
from app.algorithms.gram_schmidt import gram_schmidt
from app.algorithms.decompositions import lu_decomposition, qr_decomposition
from app.utils.cleanup import clean_matrix
from app.exceptions import LinearAlgebraError, DimensionMismatchError, NonSquareMatrixError, SingularMatrixError, LinearDependenceError, ZeroVectorError
from app.history.history_manager import HistoryManager
from app.utils.matrix_text import parse_matrix_text, matrix_to_text

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Algebra Calculator")
        self.result_view = ResultView()
        self.current_result = None

    #------ Keyboard Shortcuts ------
        self.calculate_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.calculate_shortcut.activated.connect(self.calculate)
        self.clear_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        self.clear_shortcut.activated.connect(self.clear_inputs)
        self.calculate_enter_shortcut = QShortcut(QKeySequence("Ctrl+Enter"),self)
        self.calculate_enter_shortcut.activated.connect(self.calculate)
        self.copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.copy_shortcut.activated.connect(self.copy_result)
        self.paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.paste_shortcut.activated.connect(self.paste_matrix_a)

    #------ History ------
        self.history_manager = HistoryManager()
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.show_history_entry)
        self.clear_history_button = QPushButton("Clear History")
        self.clear_history_button.clicked.connect(self.clear_history)

    #------ Step View ------
        self.step_view = StepView()

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
              "Gaussian Elimination",
              "RREF",
              "Determinant",
              "Inverse",
              "Gram-Schmidt",
              "LU Decomposition",
              "QR Decomposition",
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

    #------ Import / Export ------
        self.import_button = QPushButton("Import Matrix")
        self.import_button.clicked.connect(self.import_matrix)

        self.export_button = QPushButton("Export Result")
        self.export_button.clicked.connect(self.export_result)


    #------ Main layout ------
        layout = QVBoxLayout()
        layout.addWidget(self.import_button)
        layout.addWidget(self.export_button)

        layout.addWidget(QLabel("Matrix A"))
        layout.addLayout(matrix_a_layout)
        layout.addWidget(self.matrix_a_editor)
        layout.addWidget(self.read_matrix_a_button)

        layout.addLayout(operation_layout)
        layout.addWidget(self.scalar_widget)

        layout.addWidget(self.matrix_b_widget)

        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_view)
        layout.addWidget(self.step_view)

        layout.addWidget(QLabel("History"))
        layout.addWidget(self.history_list)
        layout.addWidget(self.clear_history_button)

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
        result_is_scalar = False
        result_displayed = False
        if matrix_a is None:
            return
        try:
            if operation == "Addition":
                matrix_b = self.matrix_b_editor.get_matrix()
                if matrix_b is None:
                    return

                if (matrix_a.rows != matrix_b.rows or matrix_a.columns != matrix_b.columns):
                    QMessageBox.warning(self, "Cannot Add Matrices",
                        ("Addition requires matrices with identical dimensions.\n\n"
                            f"Matrix A: {matrix_a.rows} × {matrix_a.columns}\n"
                            f"Matrix B: {matrix_b.rows} × {matrix_b.columns}"))
                    return

                result = add(matrix_a, matrix_b)
                inputs = [matrix_a, matrix_b]
                self.step_view.clear_steps()

            elif operation == "Subtraction":
                matrix_b = self.matrix_b_editor.get_matrix()
                if matrix_b is None:
                    return
                if (matrix_a.rows != matrix_b.rows or matrix_a.columns != matrix_b.columns):
                    QMessageBox.warning(self, "Cannot Subtract Matrices",
                        ("Subtraction requires matrices with identical dimensions.\n\n"
                            f"Matrix A: {matrix_a.rows} × {matrix_a.columns}\n"
                            f"Matrix B: {matrix_b.rows} × {matrix_b.columns}"))
                    return

                result = subtract(matrix_a, matrix_b)
                inputs = [matrix_a, matrix_b]
                self.step_view.clear_steps()

            elif operation == "Scalar Multiplication":
                scalar = float(self.scalar_input.text())
                result = scalar_multiply(matrix_a, scalar)
                inputs = [matrix_a, scalar]
                self.step_view.clear_steps()

            elif operation == "Matrix Multiplication":
                matrix_b = self.matrix_b_editor.get_matrix()
                if matrix_b is None:
                    return
                if matrix_a.columns != matrix_b.rows:
                    QMessageBox.warning(self, "Cannot Multiply Matrices",
                        ("Matrix multiplication requires the number of columns "
                            "in Matrix A to equal the number of rows in Matrix B.\n\n"
                            f"Matrix A: {matrix_a.rows} × {matrix_a.columns}\n"
                            f"Matrix B: {matrix_b.rows} × {matrix_b.columns}\n\n"
                            f"{matrix_a.columns} ≠ {matrix_b.rows}"))
                    return

                result = multiply(matrix_a, matrix_b)
                inputs = [matrix_a, matrix_b]
                self.step_view.clear_steps()

            elif operation == "Transpose":
                result = transpose(matrix_a)
                inputs = [matrix_a]
                self.step_view.clear_steps()

            elif operation == "Gaussian Elimination":
                result, steps = gaussian_elimination(matrix_a, record_steps=True)
                inputs = [matrix_a]
                self.step_view.update_steps(steps)

            elif operation == "RREF":
                result, steps = rref(matrix_a, record_steps=True)
                inputs = [matrix_a]
                self.step_view.update_steps(steps)

            elif operation == "Determinant":
                result_is_scalar = True
                result, steps = determinant(matrix_a, record_steps=True)
                inputs = [matrix_a]
                self.step_view.update_steps(steps)

            elif operation == "Inverse":
                result, steps = inverse(matrix_a, record_steps=True)
                inputs = [matrix_a]
                self.step_view.update_steps(steps)

            elif operation == "Gram-Schmidt":
                vectors = [
                    Vector([
                        matrix_a[row][column]
                        for row in range(matrix_a.rows)
                    ])
                    for column in range(matrix_a.columns)
                ]

                result_vectors, steps = gram_schmidt(vectors, record_steps=True)

                result = Matrix([
                    [
                        result_vectors[column][row]
                        for column in range(len(result_vectors))
                    ]
                    for row in range(matrix_a.rows)
                ])
                inputs = [matrix_a]
                self.step_view.update_steps(steps)

            elif operation == "LU Decomposition":
                L, U, steps = lu_decomposition(matrix_a, record_steps=True)
                inputs = [matrix_a]
                self.step_view.update_steps(steps)
                self.result_view.update_matrices([("L", L), ("U", U),])
                result_displayed = True
                result = U
                self.current_result = U

            elif operation == "QR Decomposition":
                Q, R, steps = qr_decomposition(matrix_a, record_steps=True)
                inputs = [matrix_a]
                self.step_view.update_steps(steps)
                self.result_view.update_matrices([("Q", Q), ("R", R),])

                result_displayed = True
                result = R
                self.current_result = R

            else:
                return

            self.history_manager.add_entry(operation, inputs, result)
            self.history_list.addItem(f"{len(self.history_manager)}. {operation}")

            if not result_displayed:
                if result_is_scalar:
                    self.result_view.update_scalar(result)
                    self.current_result = result
                else:
                    self.result_view.update_matrix(result)
                    self.current_result = result

        except DimensionMismatchError:
            QMessageBox.warning(self, "Dimension Mismatch", "The matrix or vector dimensions are incompatible " "for this operation.")

        except NonSquareMatrixError:
            QMessageBox.warning(self, "Square Matrix Required", ("This operation requires a square matrix.\n\n" f"You entered a " f"{matrix_a.rows} × {matrix_a.columns} matrix."))

        except SingularMatrixError:
            QMessageBox.warning(self, "Singular Matrix", ("This matrix is singular, so this operation " "cannot be completed."))

        except LinearDependenceError:
            QMessageBox.warning(self, "Linearly Dependent Input", ("This operation requires linearly independent " "vectors or matrix columns."))

        except ZeroVectorError:
                QMessageBox.warning(self, "Zero Vector", "This operation cannot be performed using the zero vector.")

        except ValueError as error:
            QMessageBox.warning(self, "Invalid Input", str(error))

        except LinearAlgebraError as error:
            QMessageBox.warning(self, "Calculation Error", str(error))

    def show_history_entry(self, item):
        index = self.history_list.row(item)
        entry = self.history_manager.get_entry(index)
        self.result_view.update_matrix(entry.result)

    def clear_history(self):
        self.history_manager.clear()
        self.history_list.clear()

    def clear_inputs(self):
        matrix_a = Matrix([
            [0.0 for _ in range(self.columns_a_spinbox.value())]
            for _ in range(self.rows_a_spinbox.value())])

        matrix_b = Matrix([
            [0.0 for _ in range(self.columns_b_spinbox.value())]
            for _ in range(self.rows_b_spinbox.value())])

        self.matrix_a = matrix_a
        self.matrix_b = matrix_b

        self.matrix_a_editor.update_matrix(matrix_a)
        self.matrix_b_editor.update_matrix(matrix_b)

        self.scalar_input.setText("1.0")

        self.step_view.clear_steps()
        self.result_view.clear_result()
        self.current_result = None

    def copy_result(self):
        if self.current_result is None:
            return

        clipboard = QApplication.clipboard()

        if isinstance(self.current_result, Matrix):
            text = matrix_to_text(self.current_result)
        else:
            text = str(self.current_result)

        clipboard.setText(text)

    def paste_matrix_a(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()

        try:
            matrix = parse_matrix_text(text)
        except ValueError as error:
            QMessageBox.warning(self, "Cannot Paste Matrix", str(error))
            return

        if matrix.rows > 10 or matrix.columns > 10:
            QMessageBox.warning(self, "Matrix Too Large", "Pasted matrices cannot exceed 10 × 10.")
            return

        self.matrix_a = matrix

        # Update dimension controls
        self.rows_a_spinbox.blockSignals(True)
        self.columns_a_spinbox.blockSignals(True)

        self.rows_a_spinbox.setValue(matrix.rows)
        self.columns_a_spinbox.setValue(matrix.columns)

        self.rows_a_spinbox.blockSignals(False)
        self.columns_a_spinbox.blockSignals(False)

        # Update table
        self.matrix_a_editor.update_matrix(matrix)

    def import_matrix(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Matrix", "", "Matrix Files (*.txt *.csv);;Text Files (*.txt);;CSV Files (*.csv)")

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            matrix = parse_matrix_text(text)
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Cannot Import Matrix", str(error))
            return

        if matrix.rows > 10 or matrix.columns > 10:
            QMessageBox.warning(self, "Matrix Too Large", "Imported matrices cannot exceed 10 × 10.")
            return

        self.matrix_a = matrix

        self.rows_a_spinbox.blockSignals(True)
        self.columns_a_spinbox.blockSignals(True)

        self.rows_a_spinbox.setValue(matrix.rows)
        self.columns_a_spinbox.setValue(matrix.columns)

        self.rows_a_spinbox.blockSignals(False)
        self.columns_a_spinbox.blockSignals(False)

        self.matrix_a_editor.update_matrix(matrix)

    def export_result(self):
        if self.current_result is None:
            QMessageBox.warning(self, "No Result", "There is no result to export.")
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(self, "Export Result", "", "Text Files (*.txt);;CSV Files (*.csv)")

        if not file_path:
            return

        root, extension = os.path.splitext(file_path)

        if not extension:
            if selected_filter.startswith("CSV"):
                file_path += ".csv"
            else:
                file_path += ".txt"
        try:
            if isinstance(self.current_result, Matrix):
                if selected_filter.startswith("CSV"):
                    text = "\n".join(",".join(str(value) for value in row)
                        for row in self.current_result.data)
                else:
                    text = matrix_to_text(self.current_result)
            else:
                text = str(self.current_result)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
        except OSError as error:
            QMessageBox.warning(
                self, "Cannot Export Result", str(error))