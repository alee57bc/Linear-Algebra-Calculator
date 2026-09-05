from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QLabel, QLayout, QVBoxLayout, QGroupBox, QScrollArea, QWidget
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.utils.numeric import format_number

class StepView(QGroupBox):
    def __init__(self):
        super().__init__("Steps")

        # Outer layout for the group box
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setMinimumHeight(200)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)

        # Container inside the scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(12)
        self.content_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.content_widget.setLayout(self.content_layout)

        # Put container inside scroll area
        self.scroll_area.setWidget(self.content_widget)
        outer_layout.addWidget(self.scroll_area)
        self.empty_label = QLabel("No calculation steps yet")
        self.empty_label.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.empty_label)
        self.scroll_area.hide()

    def clear_steps(self):
        self.empty_label.show()
        self.scroll_area.hide()
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)

            if item.widget():
                item.widget().hide()
                item.widget().deleteLater()

    def update_steps(self, steps):
        self.clear_steps()
        if not steps:
            return
        self.empty_label.hide()
        self.scroll_area.show()

        for index, step in enumerate(steps, start=1):
            description = QLabel(f"Step {index}: {step.description}")
            description.setTextFormat(Qt.PlainText)
            description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            description.setWordWrap(True)
            self.content_layout.addWidget(description)
            result = step.result

            if isinstance(result, Matrix):
                formatted = [[format_number(value) for value in row] for row in result.data]
                widths = [max(len(row[col]) for row in formatted) for col in range(result.columns)]
                for row in formatted:
                    row_label = QLabel("  ".join(value.rjust(width) for value, width in zip(row, widths)))
                    row_label.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
                    self.content_layout.addWidget(row_label)

            elif isinstance(result, Vector):
                vector_label = QLabel("[" + "  ".join(format_number(value) for value in result.data) + "]")
                vector_label.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
                self.content_layout.addWidget(vector_label)

        self.content_layout.addStretch()
        self.content_layout.activate()
        self.scroll_area.verticalScrollBar().setValue(0)
        self.scroll_area.horizontalScrollBar().setValue(0)
