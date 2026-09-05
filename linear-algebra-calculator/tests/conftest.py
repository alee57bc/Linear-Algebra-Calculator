import os
from pathlib import Path
from uuid import uuid4

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Keep temporary test files out of the shared Windows temp directory."""
    if config.option.basetemp is None:
        temp_root = Path(__file__).resolve().parent / ".pytest_tmp"
        temp_root.mkdir(exist_ok=True)
        # A fresh path avoids reusing folders owned by another test process.
        config.option.basetemp = str(temp_root / f"run-{uuid4().hex}")


@pytest.fixture(scope="session")
def qapp():
    """Run widget tests without opening desktop windows."""
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    yield app
    app.processEvents()


@pytest.fixture
def widgets(qapp):
    created = []

    def create(widget_type, *args):
        widget = widget_type(*args)
        created.append(widget)
        return widget

    yield create
    for widget in reversed(created):
        widget.close()
        widget.deleteLater()
    qapp.processEvents()
