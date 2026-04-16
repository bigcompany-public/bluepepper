"""
This module provides base classes for standardizing how Qt widgets are created across BluePepper.

BluePepper widgets rely on a custom stylesheet that uses Qt's dynamic properties. When a BluePepper
widget is embedded in a host DCC (Maya, Houdini, etc.), the host application's own stylesheet
can bleed in and override BluePepper's styles.

The fix is to always wrap user widgets inside a dedicated container widget that acts as the
stylesheet boundary (see bluepepper.gui.utils.stylesheet for details). This module makes that
pattern easy to follow consistently.

Construction pattern :
 ____________      _________________     _________________
| YourWidget | -> | ContainerWidget |-> | ContainerDialog |
on close  ⤷ result -> close instruction -> close instruction

For more in-depth examples, see:
    - bluepepper.gui.widget.lab_widget.lab_widget.py
    - bluepepper.tools.demo.demo_widgets.py
    - bluepepper.software.maya.tools.demo_widgets.py
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

import qtawesome
from bluepepper.gui.utils import format_widgets, get_qt_app, stylesheet
from qtpy.QtCore import Signal
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

W = TypeVar("W", bound=QWidget)


class ContainerWidget(QWidget, Generic[W]):
    """
    A stylesheet-boundary container that wraps around the provided widget

    This class ensures that BluePepper's stylesheet is always applied to a dedicated
    container, preventing host DCC stylesheets from bleeding into BluePepper widgets.

    To properly close the widget, make sure to call the _confirm() method, that shall store the result in the result_value attribute, before closing the ContainerDialog (if the containerWidget is within one)
    The ``confirmed`` signal acts as the exit point to pass data to the ContainerDialog
    """

    confirmed = Signal(object)

    def __init__(
        self,
        widget: W,
        title: str = "",
        icon: QIcon | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.widget: W = widget
        self.result_value: object = None

        self._setup_window(title, icon)
        self._setup_layout()
        self._setup_stylesheet()

    def _setup_window(self, title: str, icon: QIcon | None) -> None:
        if title:
            self.setWindowTitle(title)
        if icon is not None:
            self.setWindowIcon(icon)

    def _setup_layout(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # This widget actually holds the stylesheet of all child widgets
        inner = QWidget()
        outer.addWidget(inner)

        self.main_layout = QVBoxLayout(inner)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.widget)

    def _setup_stylesheet(self) -> None:
        self.setStyleSheet(stylesheet)
        format_widgets(self)

    def _confirm(self, result: Any = None):
        self.result_value = result
        # re-emit the result to the optional ContainerDialog
        self.confirmed.emit(result)
        self.close()


class ContainerDialog(QDialog, Generic[W]):
    """
    A QDialog that hosts a ContainerWidget[W].
    Automatically picks up ``windowTitle`` and ``windowIcon`` from the container

    Connects to ``container.confirmed`` to store the emitted value in
    ``result_value`` and close the dialog. The user widget (or its OK button)
    is solely responsible for emitting ``confirmed`` with the appropriate value.
    """

    def __init__(
        self,
        container: ContainerWidget[W],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.container: ContainerWidget[W] = container
        self.result_value: object = None

        self._setup_window()
        self._setup_layout()
        self._setup_signals()

    def _setup_window(self) -> None:
        if self.container.windowTitle():
            self.setWindowTitle(self.container.windowTitle())
        if not self.container.windowIcon().isNull():
            self.setWindowIcon(self.container.windowIcon())

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.container)

    def _setup_signals(self) -> None:
        self.container.confirmed.connect(self._on_confirmed)

    def _on_confirmed(self, value: object) -> None:
        self.result_value = value
        self.accept()


if __name__ == "__main__":
    app = get_qt_app()
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#000000")

    class MyLineEditWidget(QWidget):
        def __init__(self, parent: QWidget | None = None) -> None:
            super().__init__(parent)

            layout = QVBoxLayout(self)
            self.label = QLabel("Enter your name:")
            self.line_edit = QLineEdit()
            self.ok_button = QPushButton("OK")
            self.ok_button.setEnabled(False)

            layout.addWidget(self.label)
            layout.addWidget(self.line_edit)
            layout.addWidget(self.ok_button)

            self.line_edit.textChanged.connect(
                lambda text: self.ok_button.setEnabled(bool(text.strip()))
            )

        def get_value(self) -> str:
            return self.line_edit.text()

    user_widget = MyLineEditWidget()
    container: ContainerWidget[MyLineEditWidget] = ContainerWidget(
        user_widget, title="Enter Name", icon=icon
    )
    user_widget.ok_button.clicked.connect(
        lambda: container._confirm(user_widget.get_value())
    )

    # Dialog version
    dialog: ContainerDialog[MyLineEditWidget] = ContainerDialog(container)
    if dialog.exec():
        print(f"User entered: {str(dialog.result_value)!r}")
    else:
        print("Cancelled.")

    # # Standalone version
    # container.show()
    # app.exec()
    # if container.result_value:
    #     print(container.result_value)
    # else:
    #     print("Cancelled")
