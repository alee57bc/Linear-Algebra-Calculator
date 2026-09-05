from unittest.mock import Mock

import pytest
from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.core.matrix import Matrix
from app.exceptions import (
    DimensionMismatchError, NonSquareMatrixError, SingularMatrixError,
    LinearDependenceError, ZeroVectorError, LinearAlgebraError,
)
from app.ui.new_window import MainWindow


@pytest.fixture
def window(widgets, monkeypatch):
    window = widgets(MainWindow)
    # No modal dialogs can block an unattended test run.
    window.warning = Mock()
    monkeypatch.setattr(QMessageBox, "warning", window.warning)
    return window


@pytest.mark.parametrize("operation", [
    "Addition", "Subtraction", "Scalar Multiplication", "Matrix Multiplication",
    "Transpose", "Gaussian Elimination", "RREF", "Determinant", "Inverse",
    "Gram-Schmidt", "LU Decomposition", "QR Decomposition", "Eigenvalues",
    "Eigenvectors", "Diagonalization",
])
def test_calculate_and_restore_history(window, operation):
    window.matrix_a_panel.set_matrix(Matrix([[2, 1], [0, 3]]))
    window.matrix_b_panel.set_matrix(Matrix([[1, 0], [0, 1]]))
    if window.operation_selector.findText(operation) < 0:
        window.tabs.setCurrentIndex(1)
    window.operation_selector.setCurrentText(operation)
    window.scalar_input.setText("2")
    window.calculate()
    window.warning.assert_not_called()
    assert window.current_result is not None
    assert len(window.history_manager) == window.history_list.count() == 1
    entry = window.history_manager.get_entry(0)
    assert entry.operation == operation
    window.clear_inputs()
    assert window.current_result is None
    assert window.matrix_a_panel.get_matrix() == Matrix([[0, 0], [0, 0]])
    assert len(window.history_manager) == 1
    window.show_history_entry(window.history_list.item(0))
    assert window.current_result is entry.result
    assert window.operation_selector.currentText() == operation
    assert window.matrix_a_panel.get_matrix() == Matrix([[2, 1], [0, 3]])
    if operation == "Scalar Multiplication":
        assert float(window.scalar_input.text()) == 2
    window.clear_history()
    assert len(window.history_manager) == window.history_list.count() == 0


@pytest.mark.parametrize("error, title", [
    (DimensionMismatchError, "Dimension Mismatch"),
    (NonSquareMatrixError, "Square Matrix Required"),
    (SingularMatrixError, "Singular Matrix"),
    (LinearDependenceError, "Linearly Dependent Input"),
    (ZeroVectorError, "Zero Vector"),
    (ValueError, "Invalid Input"),
    (LinearAlgebraError, "Calculation Error"),
])
def test_calculation_errors_warn_without_adding_history(window, monkeypatch, error, title):
    monkeypatch.setattr(window.controller, "calculate", Mock(side_effect=error("failure")))
    window.calculate()
    assert window.warning.call_args.args[1] == title
    assert len(window.history_manager) == 0
    assert window.current_result is None


@pytest.mark.parametrize("panel", ["matrix_a_panel", "matrix_b_panel"])
def test_invalid_matrix_stops_calculation(window, monkeypatch, panel):
    monkeypatch.setattr(getattr(window, panel), "get_matrix", lambda: None)
    calculate = Mock()
    monkeypatch.setattr(window.controller, "calculate", calculate)
    window.calculate()
    calculate.assert_not_called()


def test_operation_controls_and_invalid_scalar(window):
    assert not window.matrix_b_panel.isHidden()
    assert window.scalar_widget.isHidden()
    window.operation_selector.setCurrentText("Scalar Multiplication")
    assert window.matrix_b_panel.isHidden()
    assert not window.scalar_widget.isHidden()
    window.scalar_input.setText("invalid")
    window.calculate()
    assert window.warning.call_args.args[1] == "Invalid Scalar"
    assert len(window.history_manager) == 0


def test_copy_and_paste(window, qapp):
    clipboard = qapp.clipboard()
    clipboard.setText("unchanged")
    window.copy_result()
    assert clipboard.text() == "unchanged"
    window.current_result = Matrix([[1, 2], [3, 4]])
    window.copy_result()
    assert clipboard.text() == "1 2\n3 4"
    window.paste_matrix_a()
    assert window.matrix_a_panel.get_matrix() == window.current_result
    window.current_result = 7
    window.copy_result()
    assert clipboard.text() == "7"


@pytest.mark.parametrize("text, title", [
    ("invalid", "Cannot Paste Matrix"),
    (" ".join(["1"] * 11), "Matrix Too Large"),
])
def test_paste_rejects_invalid_or_oversized_data(window, qapp, text, title):
    original = window.matrix_a_panel.get_matrix()
    qapp.clipboard().setText(text)
    window.paste_matrix_a()
    assert window.warning.call_args.args[1] == title
    assert window.matrix_a_panel.get_matrix() == original


def test_import_matrix(window, monkeypatch, tmp_path):
    path = tmp_path / "matrix.csv"
    path.write_text("1,2\n3,4", encoding="utf-8")
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args: (str(path), ""))
    window.import_matrix()
    assert window.matrix_a_panel.get_matrix() == Matrix([[1, 2], [3, 4]])
    window.warning.assert_not_called()


@pytest.mark.parametrize("contents, title", [
    ("invalid", "Cannot Import Matrix"),
    (" ".join(["1"] * 11), "Matrix Too Large"),
    (None, "Cannot Import Matrix"),
])
def test_import_errors(window, monkeypatch, tmp_path, contents, title):
    path = tmp_path / "matrix.txt"
    if contents is not None:
        path.write_text(contents, encoding="utf-8")
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args: (str(path), ""))
    window.import_matrix()
    assert window.warning.call_args.args[1] == title


@pytest.mark.parametrize("result, file_filter, suffix, expected", [
    (Matrix([[1, 2]]), "CSV Files (*.csv)", ".csv", "1,2"),
    (Matrix([[1, 2]]), "Text Files (*.txt)", ".txt", "1 2"),
    (3.5, "Text Files (*.txt)", ".txt", "3.5"),
])
def test_export_result(window, monkeypatch, tmp_path, result, file_filter, suffix, expected):
    path = tmp_path / "result"
    window.current_result = result
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args: (str(path), file_filter))
    window.export_result()
    assert path.with_suffix(suffix).read_text(encoding="utf-8") == expected
    window.warning.assert_not_called()


def test_export_errors_and_cancelled_dialogs(window, monkeypatch, tmp_path):
    window.export_result()
    assert window.warning.call_args.args[1] == "No Result"
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args: ("", ""))
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args: ("", ""))
    window.warning.reset_mock()
    window.import_matrix()
    window.current_result = Matrix([[1]])
    window.export_result()
    window.warning.assert_not_called()
    path = tmp_path / "missing" / "result.txt"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args: (str(path), "Text Files (*.txt)"))
    window.export_result()
    assert window.warning.call_args.args[1] == "Cannot Export Result"
