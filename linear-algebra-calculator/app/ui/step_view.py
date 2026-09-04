from PySide6.QtWidgets import QLabel, QVBoxLayout, QGroupBox, QScrollArea, QWidget

class StepView(QGroupBox):
    def __init__(self):
        super().__init__()

        # Outer layout for the group box
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(200)
        self.scroll_area.setMaximumHeight(400)

        # Container inside the scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        # Put container inside scroll area
        self.scroll_area.setWidget(self.content_widget)
        outer_layout.addWidget(self.scroll_area)

    def clear_steps(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    def update_steps(self, steps):
        self.clear_steps()

        for index, step in enumerate(steps, start=1):
            description = QLabel(f"Step {index}: {step.description}")
            self.content_layout.addWidget(description)

            for row in step.matrix.data:
                row_label = QLabel("  ".join(str(value) for value in row))
                self.content_layout.addWidget(row_label)