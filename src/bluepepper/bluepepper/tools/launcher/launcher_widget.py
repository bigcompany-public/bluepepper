from __future__ import annotations

import logging
import sys

from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QApplication,
    QListView,
    QListWidget,
    QListWidgetItem,
    QWidget,
)

from bluepepper.gui.utils import format_widgets, get_icon, get_stylesheet
from bluepepper.helpers.run_callable import run_callable
from bluepepper.logger import init_logging
from bluepepper.tools.launcher.launcher_config import (
    DefaultLauncherConfig,
    LauncherItem,
)
from bluepepper.tools.launcher.ui_launcher_widget import Ui_launcher_widget


class LauncherWidget(Ui_launcher_widget):
    """
    This class represents the main widget of the tool "launcher", used to
    open the various softwares and tools used on the project
    """

    def __init__(
        self,
        parent: QWidget,
    ):
        self._parent = parent
        self.tool_config = DefaultLauncherConfig
        self.setup_ui()
        self.setup_signals()
        self.setup_initial_state()

    def setup_ui(self):
        """Adds widgets to the main widget"""
        self.setupUi(self._parent)
        self._parent.setStyleSheet(get_stylesheet())
        format_widgets(self._parent)

        # Apps List
        self.list_apps.setViewMode(QListView.IconMode)
        self.list_apps.setIconSize(self.icon_size)
        self.list_apps.setWordWrap(True)
        self.list_apps.setSpacing(5)
        self.list_apps.setUniformItemSizes(True)
        self.list_apps.setResizeMode(QListWidget.Adjust)

        # Tools List
        self.list_tools.setViewMode(QListView.IconMode)
        self.list_tools.setIconSize(self.icon_size)
        self.list_tools.setWordWrap(True)
        self.list_tools.setSpacing(5)
        self.list_tools.setUniformItemSizes(True)
        self.list_tools.setResizeMode(QListWidget.Adjust)

    def setup_signals(self):
        self.list_apps.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.list_tools.itemDoubleClicked.connect(self.on_item_double_clicked)

    def setup_initial_state(self):
        self.add_app_items()
        self.add_tool_items()

    @property
    def icon_size(self) -> QSize:
        size = 70
        return QSize(size, size)

    def add_app_items(self):
        for app in self.tool_config.apps:
            self.add_app_item(app)

    def add_app_item(self, app: LauncherItem):
        app_item = AppItem(app, self)
        self.list_apps.addItem(app_item)

    def on_item_double_clicked(self, item: AppItem):
        logging.info(f"Launching: {item.app.label}")
        run_callable(
            module=item.app.module,
            function=item.app.function,
        )

    def add_tool_items(self):
        for tool in self.tool_config.tools:
            self.add_tool_item(tool)

    def add_tool_item(self, tool: LauncherItem):
        tool_item = ToolItem(tool, self)
        self.list_tools.addItem(tool_item)


class AppItem(QListWidgetItem):
    def __init__(self, app: LauncherItem, main_widget: LauncherWidget):
        self.app = app
        self.main_widget = main_widget
        icon = QIcon(get_icon(self.app.icon).as_posix())
        super().__init__()
        self.setText(self.app.label)
        self.setIcon(icon)
        if self.app.tooltip:
            self.setToolTip(self.app.tooltip)


class ToolItem(QListWidgetItem):
    def __init__(self, app: LauncherItem, main_widget: LauncherWidget):
        self.app = app
        self.main_widget = main_widget
        icon = QIcon(get_icon(self.app.icon).as_posix())
        super().__init__()
        self.setText(self.app.label)
        self.setIcon(icon)
        if self.app.tooltip:
            self.setToolTip(self.app.tooltip)


def show_widget():
    """This function pops the main window open"""
    # Create a QApplication instance if it does not exist yet
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = QWidget()
    ui = LauncherWidget(parent=window)
    window.show()
    app.exec_()


if __name__ == "__main__":
    init_logging(app="bluepepperApp")
    show_widget()
