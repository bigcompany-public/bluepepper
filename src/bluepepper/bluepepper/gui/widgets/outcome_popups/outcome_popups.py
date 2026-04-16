"""
status_dialogs.py
-----------------
Consolidated module for success and error feedback dialogs.

Provides:
- ``SuccessWidget`` / ``ErrorWidget``  — plain QWidget wrappers around the
  QtDesigner-generated UIs, ready to drop into a ContainerWidget.
- ``show_success`` / ``show_error``    — convenience one-liner functions.
- ``OutcomePopup``                    — context manager that pops the right
  dialog depending on whether the block raised an exception.

All dialogs are built with the ContainerWidget / ContainerDialog pattern so
BluePepper's stylesheet boundary is always respected.
"""

from __future__ import annotations

import os
import traceback as trc
from types import TracebackType
from typing import Type

import pyperclip
import qtawesome
from bluepepper.gui.utils import get_qt_app, get_sound, get_theme
from bluepepper.gui.widgets.container import ContainerDialog, ContainerWidget
from bluepepper.gui.widgets.outcome_popups.ui_error_widget import Ui_error_widget
from bluepepper.gui.widgets.outcome_popups.ui_success_widget import Ui_success_widget
from bluepepper.tools.helpme.helpme_button import HelpMeButton
from bluepepper.tools.helpme.helpme_widget import show_dialog as show_helpme_dialog
from qtpy.QtCore import Qt, QUrl
from qtpy.QtWidgets import QWidget

try:
    from PySide6.QtMultimedia import QSoundEffect
except ImportError:
    from PySide2.QtMultimedia import QSoundEffect


def _play(filename: str, volume: float) -> QSoundEffect:
    effect = QSoundEffect()
    path = get_sound(filename)
    effect.setSource(QUrl.fromLocalFile(path.as_posix()))
    effect.setVolume(volume)
    effect.play()
    return effect  # caller must keep a reference alive


class SuccessWidget(QWidget):
    """
    Thin QWidget shell around the QtDesigner success UI.
    Intended to be wrapped in a ContainerWidget / ContainerDialog.
    """

    def __init__(
        self,
        message: str = "",
        sound: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._effect: QSoundEffect | None = None
        self._ui = Ui_success_widget()
        self._ui.setupUi(self)

        if message:
            self._ui.label_message.setText(message)

        self._ui.button_ok.clicked.connect(self._on_ok)

        if sound:
            self._effect = _play("success2.wav", volume=0.1)

    def _on_ok(self) -> None:
        self.window().close()


class ErrorWidget(QWidget):
    """
    Widget that shows an error and its traceback.
    Also contains a HelpMeButton that helps the end user to easily create tickets
    """

    def __init__(
        self,
        error: str = "",
        traceback: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._effect: QSoundEffect | None = None
        self._error = error.strip()
        self._traceback = traceback.strip()

        self._ui = Ui_error_widget()
        self._ui.setupUi(self)

        self._ui.label_error.setMaximumWidth(2000)
        self._ui.label_error.setWordWrap(True)
        self._ui.label_traceback.setMaximumWidth(2000)
        self._ui.label_traceback.setWordWrap(True)

        if self._error:
            self._ui.label_error.setText(self._error)
        if self._traceback:
            self._ui.label_traceback.setText(self._traceback)

        self._ui.button_ok.clicked.connect(self._on_ok)
        self._ui.button_copy.clicked.connect(self._on_copy)

        self._help_button = HelpMeButton()
        self._ui.top_widget_layout.addWidget(self._help_button)

        self._help_button._btn.clicked.connect(self._on_help)

        self._effect = _play("error1.wav", volume=0.15)

    def _on_ok(self) -> None:
        self.window().close()

    def _on_copy(self) -> None:
        if self._traceback:
            pyperclip.copy(self._traceback)

    def _on_help(self) -> None:
        window = self.window()
        window.showMinimized()
        show_helpme_dialog(error=self._error, traceback=self._traceback)
        window.showNormal()


def show_success(message: str = "", sound: bool = False) -> None:
    """Pop a success dialog. Safe to call from any context."""
    app = get_qt_app()

    color = get_theme()["ok"]
    icon = qtawesome.icon("ei.ok-sign", color=color)

    widget = SuccessWidget(message=message, sound=sound)
    container: ContainerWidget[SuccessWidget] = ContainerWidget(
        widget=widget,
        title="Success",
        icon=icon,
    )
    dialog: ContainerDialog[SuccessWidget] = ContainerDialog(container=container)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
    dialog.exec_()


def show_error(error: str = "", traceback: str = "") -> None:
    """Pop an error dialog. Safe to call from any context."""
    app = get_qt_app()

    color = get_theme()["error"]
    icon = qtawesome.icon("fa6s.circle-xmark", color=color)

    widget = ErrorWidget(error=error, traceback=traceback)
    container: ContainerWidget[ErrorWidget] = ContainerWidget(
        widget=widget,
        title="Error",
        icon=icon,
    )
    dialog: ContainerDialog[ErrorWidget] = ContainerDialog(container=container)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
    dialog.exec_()


class OutcomePopup:
    """
    Context manager that shows a success or error dialog based on whether
    the managed block raised an exception.

    Usage::

        with OutcomePopup(success_message="Done!", sound=True) as op:
            do_work()
            op.success_message = "Done — processed 42 items."

        # Custom error message:
        with OutcomePopup(error_message="Import failed") as op:
            risky_import()
    """

    def __init__(
        self,
        show_success_popup: bool = True,
        success_message: str = "",
        error_message: str = "",
        sound: bool = False,
    ) -> None:
        self.show_success_popup = show_success_popup
        self.success_message = success_message
        self.error_message = error_message
        self.sound = sound

    def __enter__(self) -> OutcomePopup:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        if exc_value is not None:
            message = self.error_message or str(exc_value)
            show_error(error=message, traceback=trc.format_exc())
            return False  # let the exception propagate

        if self.show_success_popup and not int(os.environ.get("BIG_NOGUI", 0)):
            show_success(message=self.success_message, sound=self.sound)

        return None


if __name__ == "__main__":
    os.environ["BIG_NOGUI"] = "0"
    app = get_qt_app()

    # Success
    with OutcomePopup(show_success_popup=True, sound=True) as op:
        print("doing work…")
        op.success_message = "Everything went smoothly."

    # Error
    with OutcomePopup(error_message="Something went wrong") as op:
        raise ValueError("Deliberate test error")
