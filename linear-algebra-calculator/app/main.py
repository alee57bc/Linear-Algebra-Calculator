import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication
from app.ui.new_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    palette = app.palette()
    for role, color in {
        QPalette.Window: "#ffffff",
        QPalette.Base: "#ffffff",
        QPalette.AlternateBase: "#f8fafc",
        QPalette.Button: "#f1f5f9",
        QPalette.WindowText: "#1e293b",
        QPalette.Text: "#1e293b",
        QPalette.ButtonText: "#1e293b",
        QPalette.Mid: "#cbd5e1",
        QPalette.Highlight: "#2563eb",
        QPalette.HighlightedText: "#ffffff",
        QPalette.PlaceholderText: "#64748b",
        QPalette.ToolTipBase: "#ffffff",
        QPalette.ToolTipText: "#1e293b",
    }.items():
        palette.setColor(role, QColor(color))
    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText):
        palette.setColor(QPalette.Disabled, role, QColor("#64748b"))
    app.setPalette(palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
