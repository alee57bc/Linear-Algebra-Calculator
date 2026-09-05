import os
from PySide6.QtWidgets import QApplication, QComboBox, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QTabBar, QVBoxLayout, QWidget
from PySide6.QtGui import  QKeySequence, QShortcut
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.ui.result_view import ResultView
from app.ui.step_view import StepView
from app.history.history_manager import HistoryManager
from app.utils.matrix_text import parse_matrix_text, matrix_to_text
from app.ui.matrix_panel import MatrixPanel
from app.ui.calculations import CalculationController
from app.exceptions import LinearAlgebraError, DimensionMismatchError, NonSquareMatrixError, SingularMatrixError, LinearDependenceError, ZeroVectorError
from app.utils.numeric import format_number

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Algebra Calculator")
        self.resize(1200, 850)
        self.setMinimumSize(950, 700)
        self.current_result = None
        self.controller = CalculationController()

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

    #------ Tabs ------
        self.tabs = QTabBar()
        self.tabs.addTab("Basic Operations")
        self.tabs.addTab("Linear Algebra")
        self.tabs.currentChanged.connect(self.update_operation_tab)

    #------ Make Matrixes ------
        self.matrix_a_panel = MatrixPanel("Matrix A")
        self.matrix_b_panel = MatrixPanel("Matrix B")

    #------ Operations ------
        self.operation_selector = QComboBox()

        #scalar operations
        self.scalar_input = QLineEdit()
        self.scalar_input.setPlaceholderText("Enter Scalar")
        self.scalar_input.setText("1.0")
        scalar_layout = QHBoxLayout()
        scalar_layout.addWidget(QLabel("Scalar: "))
        scalar_layout.addWidget(self.scalar_input)
        self.scalar_widget = QWidget()
        self.scalar_widget.setLayout(scalar_layout)

        #calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

        #operation layout
        operation_layout = QVBoxLayout()
        operation_layout.addWidget(self.operation_selector)
        operation_layout.addWidget(self.scalar_widget)
        operation_layout.addWidget(self.calculate_button)

        self.operation_group = QGroupBox("Operation")
        self.operation_group.setLayout(operation_layout)
        self.operation_selector.currentTextChanged.connect(self.update_operation_ui)

    #------ Result ------
        self.result_view = ResultView()
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_view)
        self.result_group = QGroupBox("Result")
        self.result_group.setLayout(result_layout)

    #------ Step View ------
        self.step_view = StepView()

    #------ History ------
        self.history_manager = HistoryManager()
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.show_history_entry)
        self.clear_history_button = QPushButton("Clear History")
        self.clear_history_button.clicked.connect(self.clear_history)

        history_layout = QVBoxLayout()
        history_layout.addWidget(self.history_list)
        history_layout.addWidget(self.clear_history_button)
        self.history_group = QGroupBox("History")
        self.history_group.setLayout(history_layout)

    #------ Import / Export ------
        self.import_button = QPushButton("Import Matrix")
        self.import_button.clicked.connect(self.import_matrix)

        self.export_button = QPushButton("Export Result")
        self.export_button.clicked.connect(self.export_result)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.import_button)
        file_layout.addWidget(self.export_button)

    #------ Main grid ------
        content_layout = QGridLayout()
        content_layout.addWidget(self.matrix_a_panel, 0, 0)

        content_layout.addWidget(self.operation_group, 0, 1)

        content_layout.addWidget(self.matrix_b_panel, 0, 2)

        content_layout.addWidget(self.result_group, 1, 1)

        content_layout.addWidget(self.step_view, 2, 0, 1, 2)

        content_layout.addWidget(self.history_group, 2, 2)

        content_layout.setColumnStretch(0, 3)
        content_layout.setColumnStretch(1, 2)
        content_layout.setColumnStretch(2, 3)

        content_layout.setRowStretch(0, 3)
        content_layout.setRowStretch(1, 2)
        content_layout.setRowStretch(2, 3)

    #------ Main outer layout ------
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(file_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        #initialize basic tab
        self.update_operation_tab(0)

#------ Tabs ------
    def update_operation_tab(self, index):
        self.operation_selector.clear()

        if index == 0:
            self.operation_selector.addItems([
                "Addition",
                "Subtraction",
                "Scalar Multiplication",
                "Matrix Multiplication",
                "Transpose",])
        else:
            self.operation_selector.addItems([
                "Gaussian Elimination",
                "RREF",
                "Determinant",
                "Inverse",
                "Gram-Schmidt",
                "LU Decomposition",
                "QR Decomposition",
                "Eigenvalues",
                "Eigenvectors",
                "Diagonalization",])
        self.update_operation_ui()

#------ Dynamic operation UI ------
    def update_operation_ui(self):
        operation = (self.operation_selector.currentText())

        needs_matrix_b = operation in [
            "Addition",
            "Subtraction",
            "Matrix Multiplication",]

        self.matrix_b_panel.setVisible(needs_matrix_b)
        needs_scalar = (operation == "Scalar Multiplication")
        self.scalar_widget.setVisible(needs_scalar)

#------ History ------
    def show_history_entry(self, item):
        index = self.history_list.row(item)
        entry = self.history_manager.get_entry(index)

        #restore inputs
        if len(entry.inputs) >= 1:
            first_input = entry.inputs[0]

            if isinstance(first_input, Matrix):
                self.matrix_a_panel.set_matrix(first_input)

        if len(entry.inputs) >= 2:
            second_input = entry.inputs[1]

            if isinstance(second_input, Matrix):
                self.matrix_b_panel.set_matrix(second_input)

            elif isinstance(second_input, (int, float)):
                self.scalar_input.setText(str(second_input))

        #restore operation
        basic_operations = [
            "Addition",
            "Subtraction",
            "Scalar Multiplication",
            "Matrix Multiplication",
            "Transpose",
        ]

        if entry.operation in basic_operations:
            self.tabs.setCurrentIndex(0)
        else:
            self.tabs.setCurrentIndex(1)

        operation_index = (self.operation_selector.findText(entry.operation))

        if operation_index >= 0:
            self.operation_selector.setCurrentIndex(operation_index)

        #restore steps
        if entry.steps:
            self.step_view.update_steps(entry.steps)
        else:
            self.step_view.clear_steps()

        #restore result
        if entry.extra_results:
            self.result_view.update_matrices(entry.extra_results)
        elif isinstance(entry.result, Matrix):
            self.result_view.update_matrix(entry.result)
        elif (isinstance(entry.result, list) and entry.result and isinstance(entry.result[0], Vector)):
            self.result_view.update_vectors(entry.result)
        elif isinstance(entry.result, list):
            self.result_view.update_values(entry.result)
        else:
            self.result_view.update_scalar(entry.result)

        self.current_result = entry.result

    def clear_history(self):
        self.history_manager.clear()
        self.history_list.clear()

#------ Clear ------
    def clear_inputs(self):
        matrix_a = Matrix([
                [0.0 for _ in range(self.matrix_a_panel.columns_spinbox.value())]
                for _ in range(self.matrix_a_panel.rows_spinbox.value())])

        matrix_b = Matrix([
            [0.0 for _ in range(self.matrix_b_panel.columns_spinbox.value())]
            for _ in range(self.matrix_b_panel.rows_spinbox.value())])

        self.matrix_a_panel.set_matrix(matrix_a)
        self.matrix_b_panel.set_matrix(matrix_b)

        self.scalar_input.setText("1.0")

        self.step_view.clear_steps()
        self.result_view.clear_result()

        self.current_result = None

#------ Copy and Paste ------
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

        self.matrix_a_panel.set_matrix(matrix)

#------ Import and Export ------
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

        self.matrix_a_panel.set_matrix(matrix)

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
                    text = "\n".join(",".join(format_number(value) for value in row)
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

#------ Calculate ------
    def calculate(self):
        operation = self.operation_selector.currentText()

        matrix_a = self.matrix_a_panel.get_matrix()

        if matrix_a is None:
            return

        matrix_b = None
        scalar = None

        # Operations that require Matrix B
        if operation in [
            "Addition",
            "Subtraction",
            "Matrix Multiplication",]:
            matrix_b = self.matrix_b_panel.get_matrix()

            if matrix_b is None:
                return

        # Scalar multiplication
        if operation == "Scalar Multiplication":
            try:
                scalar = float(self.scalar_input.text())
            except ValueError:
                QMessageBox.warning(self, "Invalid Scalar", "Enter a valid numeric scalar.")
                return

        try:
            calculation = self.controller.calculate(operation=operation, matrix_a=matrix_a, matrix_b=matrix_b, scalar=scalar,)

            #step by step
            if calculation.steps:
                self.step_view.update_steps(calculation.steps)
            else:
                self.step_view.clear_steps()

            #display result
            if calculation.extra_results:
                self.result_view.update_matrices(calculation.extra_results)
            elif isinstance(calculation.result, Matrix):
                self.result_view.update_matrix(calculation.result)
            elif (isinstance(calculation.result, list) and calculation.result and isinstance(calculation.result[0], Vector)):
                self.result_view.update_vectors(calculation.result)
            elif isinstance(calculation.result, list):
                self.result_view.update_values(calculation.result)
            else:
                self.result_view.update_scalar(calculation.result)

            self.current_result = (calculation.result)

            #history
            inputs = [matrix_a]

            if matrix_b is not None:
                inputs.append(matrix_b)

            if scalar is not None:
                inputs.append(scalar)

            self.history_manager.add_entry(operation, inputs, calculation.result, steps=calculation.steps, extra_results=calculation.extra_results)

            self.history_list.addItem(f"{len(self.history_manager)}. " f"{operation}")

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
