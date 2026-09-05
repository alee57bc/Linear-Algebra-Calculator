from unittest.mock import Mock

from PySide6.QtWidgets import QMessageBox

from app.core.matrix import Matrix
from app.core.vector import Vector
from app.results.calculation_step import CalculationStep
from app.ui.matrix_editor import MatrixEditor
from app.ui.matrix_panel import MatrixPanel
from app.ui.result_view import ResultView
from app.ui.step_view import StepView


def test_editor_reads_edits_and_missing_cells(widgets):
    editor = widgets(MatrixEditor, Matrix([[1, 2]]))
    assert editor.item(0, 0).text() == "1"
    editor.item(0, 0).setText(" -2.5 ")
    editor.takeItem(0, 1)
    assert editor.get_matrix() == Matrix([[-2.5, 0]])
    editor.update_matrix(Matrix([[3], [4]]))
    assert (editor.rowCount(), editor.columnCount()) == (2, 1)
    assert editor.get_matrix() == Matrix([[3], [4]])


def test_editor_invalid_input_warns(widgets, monkeypatch):
    warning = Mock()
    monkeypatch.setattr(QMessageBox, "warning", warning)
    editor = widgets(MatrixEditor, Matrix([[1]]))
    editor.item(0, 0).setText("invalid")
    assert editor.get_matrix() is None
    assert warning.call_args.args[1] == "Invalid Matrix Value"
    assert "row 1, column 1" in warning.call_args.args[2]


def test_panel_resize_preserves_values_and_pads_with_zero(widgets):
    panel = widgets(MatrixPanel, "A")
    panel.set_matrix(Matrix([[1, 2], [3, 4]]))
    panel.rows_spinbox.setValue(3)
    panel.columns_spinbox.setValue(3)
    assert panel.get_matrix() == Matrix([[1, 2, 0], [3, 4, 0], [0, 0, 0]])
    panel.rows_spinbox.setValue(1)
    panel.columns_spinbox.setValue(1)
    assert panel.get_matrix() == Matrix([[1]])


def test_panel_invalid_input_does_not_replace_matrix(widgets, monkeypatch):
    panel = widgets(MatrixPanel, "A")
    original = panel.matrix.copy()
    monkeypatch.setattr(panel.editor, "get_matrix", lambda: None)
    panel.change_dimensions()
    assert panel.matrix == original


def labels(layout):
    return [layout.itemAt(i).widget().text() for i in range(layout.count())
            if layout.itemAt(i).widget() is not None]


def test_result_view_replaces_each_result_type(widgets):
    view = widgets(ResultView, Matrix([[1, 2]]))
    assert labels(view.matrix_layout) == ["1", "2"]
    view.update_scalar(1j)
    assert labels(view.matrix_layout) == ["i"]
    view.update_values([2, -1j])
    assert labels(view.matrix_layout) == ["λ₁ = 2", "λ₂ = -i"]
    view.update_vectors([Vector([1, 2])])
    assert labels(view.matrix_layout) == ["v₁ = [1  2]"]
    view.update_matrices([("P", Matrix([[1]])), ("D", Matrix([[2]]))])
    assert labels(view.matrix_layout) == ["P =", "1", "D =", "2"]
    view.clear_result()
    assert view.matrix_layout.count() == 0


def test_step_view_renders_matrix_vector_and_description_only(widgets):
    view = widgets(StepView)
    view.update_steps([
        CalculationStep("Matrix", Matrix([[1, 2]])),
        CalculationStep("Vector", Vector([3, 4])),
        CalculationStep("Done", None),
    ])
    assert labels(view.content_layout) == [
        "Step 1: Matrix", "1  2", "Step 2: Vector", "[3  4]", "Step 3: Done"]
    view.update_steps([CalculationStep("New", None)])
    assert labels(view.content_layout) == ["Step 1: New"]
    view.clear_steps()
    assert view.content_layout.count() == 0


def test_eigenvalue_steps_scroll_and_restart_at_top(widgets, qapp):
    from PySide6.QtCore import Qt
    from app.algorithms.eigen import eigenvalues

    view = widgets(StepView)
    view.resize(340, 250)
    view.show()
    _, steps = eigenvalues(Matrix([[2, 1], [0, 3]]), record_steps=True)
    view.update_steps(steps)
    qapp.processEvents()
    scrollbar = view.scroll_area.verticalScrollBar()
    assert scrollbar.isVisible()
    assert scrollbar.maximum() > 0
    for index, step in enumerate(steps):
        label = view.content_layout.itemAt(index).widget()
        assert label.text() == f"Step {index + 1}: {step.description}"
        assert label.textFormat() == Qt.PlainText
        assert label.height() >= label.heightForWidth(label.width())
    scrollbar.setValue(scrollbar.maximum())
    view.update_steps(steps)
    qapp.processEvents()
    assert scrollbar.value() == 0
