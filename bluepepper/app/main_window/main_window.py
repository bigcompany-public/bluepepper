from __future__ import annotations

import ctypes
import json
import logging
import random
import sys
import traceback
from importlib import import_module
from pathlib import Path
from threading import Thread
from typing import Any, Callable

from PySide6.QtGui import QCloseEvent
import qtawesome
from qtpy.QtCore import QSize, Qt, QTimer
from qtpy.QtGui import QIcon, QMouseEvent, QPixmap
from qtpy.QtWidgets import QLabel, QPushButton, QWidget

from bluepepper.app.api.fastapi_bridge import fastapi_bridge
from bluepepper.app.api.fastapi_server import run_server_as_daemon
from bluepepper.app.main_window.frameless_window import FramelessMainWindow
from bluepepper.app.main_window.ui_main_window import Ui_bluepepper_app_widget
from bluepepper.console import BluePepperConsole
from bluepepper.core import init_logging, root_dir, version
from bluepepper.gui.utils import format_widgets, get_icon, get_qt_app, get_stylesheet, get_theme
from bluepepper.gui.widgets.outcome_popups import show_error
from conf.fastapi import FastApiSettings
from conf.project import ProjectSettings
from bluepepper.tools.batcher.batcher_widget import BatcherWidget

_PAGES_DIR = Path(__file__).parent
_DOUBLE_CLICK_MS = 150
_MENU_BUTTON_SIZE = 40
_MENU_ICON_SIZE = 28
_TOPBAR_BUTTON_SIZE = 35
_TOPBAR_ICON_SCALE = 1.1


class BluePepperApp(FramelessMainWindow):
    """Main application window for BluePepper."""

    def __init__(self) -> None:
        super().__init__()
        self.page_buttons: list[PageWidgetButton] = []
        self.page_widgets: list[QWidget] = []
        self.dragging = False
        self.click_count = 0
        self.colors = get_theme()

        self._setup_central_widget()
        self._setup_ui()
        self._setup_signals()
        self._setup_fastapi()
        self.setStyleSheet("border:none")

        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self._on_doubleclick_timeout)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self.ui.frame_topbar.underMouse():
            self.dragging = True
            self.click_count += 1
            self.click_timer.start(_DOUBLE_CLICK_MS)
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.dragging:
            return
        if self.isMaximized():
            self.toggle_maximized()
        else:
            self.window().move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def _on_doubleclick_timeout(self) -> None:
        if self.click_count == 2:
            self.toggle_maximized()
        self.click_count = 0

    def _setup_central_widget(self) -> None:
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(get_stylesheet())
        self.setWindowTitle("BluePepper")
        self.setWindowIcon(QIcon(get_icon("bluepepper.ico").as_posix()))
        self.setCentralWidget(self.central_widget)

    def _setup_signals(self) -> None:
        self.ui.pb_close.clicked.connect(self.close)
        self.ui.pb_minimize.clicked.connect(self.showMinimized)
        self.ui.pb_maximize.clicked.connect(self.toggle_maximized)

    def _setup_fastapi(self) -> None:
        run_server_as_daemon(port=FastApiSettings.fastapi_port)
        fastapi_bridge.payload.connect(self._handle_fastapi_query)

    def _handle_fastapi_query(self, payload: dict[str, Any]) -> None:
        """Dispatch an incoming FastAPI request to the appropriate function."""
        logging.info("FastAPI Request received: %s", payload)

        func_str: str = payload.pop("_function")
        kwargs = {**payload, "bluepepper_app": self}

        from bluepepper.app.api import fastapi_functions

        func: Callable = getattr(fastapi_functions, func_str)
        Thread(target=func, kwargs=kwargs, daemon=True).start()

    def _setup_ui(self) -> None:
        self.setMinimumSize(QSize(600, 350))
        self.ui = Ui_bluepepper_app_widget()
        self.ui.setupUi(self.central_widget)
        self.ui.label_version.setText(f"v{version}")
        image_path = get_icon("bluepepper_transparent.png")
        pixmap = QPixmap(image_path).scaledToWidth(24, Qt.SmoothTransformation)
        icon_label = QLabel()
        icon_label.setPixmap(pixmap)
        self.ui.layout_icon.addWidget(icon_label)
        format_widgets(self.ui.widget_main)

        self._add_topbar_buttons()
        self.set_random_catchphrase()
        self._add_pages()

        # Minimize/restore workaround for a Qt frame-reappearance bug
        self.showMinimized()
        self.showNormal()

    def _make_topbar_icon(self, icon_id: str) -> QIcon:
        return qtawesome.icon(icon_id, scale_factor=_TOPBAR_ICON_SCALE, color=self.colors["icon_color"])

    def _add_topbar_buttons(self) -> None:
        for button, icon_id in (
            (self.ui.pb_close, "msc.chrome-close"),
            (self.ui.pb_minimize, "msc.chrome-minimize"),
            (self.ui.pb_maximize, "msc.chrome-maximize"),
        ):
            button.setFixedSize(_TOPBAR_BUTTON_SIZE, _TOPBAR_BUTTON_SIZE)
            button.setIcon(self._make_topbar_icon(icon_id))

    def _add_pages(self) -> None:
        """Load page/button definitions from JSON and populate the sidebar."""

        def _load(filename: str, layout) -> list[dict]:
            pages = json.loads((_PAGES_DIR / filename).read_text())
            for page in pages:
                page["destination_layout"] = layout
            return pages

        app_pages = _load("pages.json", self.ui.frame_apps.layout())
        settings_pages = _load("pages_settings.json", self.ui.frame_settings.layout())
        all_pages = app_pages + settings_pages

        self.ui.frame_apps.layout().removeItem(self.ui.spacer_apps)  # type: ignore[arg-type]

        first_page_button: PageWidgetButton | None = None
        for index, page in enumerate(all_pages):
            icon = qtawesome.icon(
                page["icon"],
                scale_factor=page["icon_size"],
                color=self.colors["icon_color"],
            )
            if page.get("is_widget", True):
                btn = PageWidgetButton(
                    parent=self,
                    page_index=index,
                    icon=icon,
                    tooltip=page.get("tooltip", ""),
                    module=page["module"],
                    widget_class=page["class"],
                )
                self.page_buttons.append(btn)
                if first_page_button is None:
                    first_page_button = btn
            else:
                btn = FunctionButton(
                    parent=self,
                    icon=icon,
                    tooltip=page.get("tooltip", ""),
                    module=page["module"],
                    func=page["function"],
                )
            page["destination_layout"].addWidget(btn)

        self.ui.frame_apps.layout().addItem(self.ui.spacer_apps)

        if first_page_button is not None:
            first_page_button.setFocus()

    def toggle_maximized(self) -> None:
        """Toggle between maximized and normal window state."""
        self.set_random_catchphrase()
        self.showNormal() if self.isMaximized() else self.showMaximized()

    def set_random_catchphrase(self) -> None:
        """Pick a random catchphrase and display it in the topbar label."""
        phrases: list[str] = json.loads((root_dir / "conf/catchphrases.json").read_text("utf-8"))
        self.ui.label_important_content.setText(random.choice(phrases))

        if str(random.random()).endswith("00"):
            self.ui.label_important_content.setText("Mark my words ashen one, you remain among the accursed.")

    def showNormal(self) -> None:
        self.set_random_catchphrase()
        super().showNormal()

    def closeEvent(self, event: QCloseEvent) -> None:
        # Check running threads in the batcher
        batcher_widget = None
        for widget in self.page_widgets:
            if isinstance(widget, BatcherWidget):
                batcher_widget = widget
        
        if not batcher_widget:
            return super().closeEvent(event)
        
        active_jobs = batcher_widget.active_job_widgets
        for job_widget in active_jobs:
            logging.warning(f"Terminating Batcher Job : {job_widget.job_data.name}")
            job_widget.terminate_job()

        return super().closeEvent(event)


class MenuButton(QPushButton):
    """Base class for sidebar navigation buttons."""

    def __init__(
        self,
        parent: BluePepperApp,
        icon: QIcon,
        module: str,
        tooltip: str = "",
    ) -> None:
        super().__init__(parent)
        self._parent = parent
        self.module = module
        self.setIcon(icon)
        self.setFixedSize(_MENU_BUTTON_SIZE, _MENU_BUTTON_SIZE)
        self.setIconSize(QSize(_MENU_ICON_SIZE, _MENU_ICON_SIZE))
        self.setProperty("type", "menuItem")
        self.setToolTip(tooltip)
        self.clicked.connect(self.button_clicked)

    def button_clicked(self) -> None:
        """Handle button click. Override in subclasses."""


class PageWidgetButton(MenuButton):
    """Sidebar button that switches the stacked widget to a specific page."""

    def __init__(
        self,
        parent: BluePepperApp,
        page_index: int,
        icon: QIcon,
        widget_class: str,
        module: str,
        tooltip: str = "",
    ) -> None:
        self.bluepepper_app = parent
        self.widget_class = widget_class
        self.page_index = page_index
        self.page_widget: QWidget | None = None
        super().__init__(self.bluepepper_app, icon, module, tooltip)
        self._initialize_widget()

    def _initialize_widget(self) -> None:
        """Instantiate the page widget and register it in the stacked widget."""
        module = import_module(self.module)
        cls = getattr(module, self.widget_class)
        container = QWidget()
        self.page_widget: QWidget = cls(container)
        self.page_widget.bluepepper_app = self._parent
        self.bluepepper_app.page_widgets.append(self.page_widget)
        self._parent.ui.stackedWidget.addWidget(container)

    def button_clicked(self) -> None:
        self._parent.ui.stackedWidget.setCurrentIndex(self.page_index)


class FunctionButton(QPushButton):
    """Sidebar button that calls an arbitrary function on click."""

    def __init__(
        self,
        parent: BluePepperApp,
        icon: QIcon,
        module: str | None = None,
        func: str | None = None,
        tooltip: str = "",
    ) -> None:
        super().__init__(parent)
        self._parent = parent
        self.module = module
        self.func = func
        self.setIcon(icon)
        self.setFixedSize(_MENU_BUTTON_SIZE, _MENU_BUTTON_SIZE)
        self.setIconSize(QSize(_MENU_ICON_SIZE, _MENU_ICON_SIZE))
        self.setProperty("type", "menuItem")
        self.setToolTip(tooltip)
        self.setFocusPolicy(Qt.NoFocus)
        self.clicked.connect(self.button_clicked)

    def button_clicked(self) -> None:
        func: Callable = getattr(import_module(self.module), self.func)
        func()


def except_hook(exc_type: type, exc_value: BaseException, exc_traceback: Any) -> None:
    """Global exception handler: show console and error popup."""
    console = BluePepperConsole()
    console.show()
    formatted = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.error(formatted)
    show_error(error=str(exc_value), traceback=formatted)


def show_main_window() -> None:
    """Bootstrap and display the BluePepper application window."""
    sys.excepthook = except_hook
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"bluepepper.{ProjectSettings.project_name}")
    app = get_qt_app()
    main_window = BluePepperApp()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    init_logging("bluepepperApp")
    show_main_window()
