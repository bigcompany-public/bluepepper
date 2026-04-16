from __future__ import annotations

from qtpy.QtWidgets import (
    QApplication,
    QDialog,
    QLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from bluepepper.core import init_logging
from bluepepper.gui.utils import format_widgets, get_stylesheet
from bluepepper.tools.browser.browser_config import AppConfig
from bluepepper.tools.browser.browser_tab import EntityTab


class BrowserWidget(QWidget):
    def __init__(self, parent: QWidget, tool_config: AppConfig):
        super().__init__(parent)
        self._parent = parent
        self._layout: QLayout
        self.tool_config = tool_config
        self.attach_to_parent()
        self.init_ui()
        self.apply_stylesheet()

    def get_layout(self) -> QLayout:
        return self._parent.layout()  # type: ignore

    def attach_to_parent(self):
        # Create layout if needed
        if not self._parent.layout():
            self._layout = QVBoxLayout()
            self._parent.setLayout(self._layout)
        else:
            self._layout = self.get_layout()

        # Create main widget, who will contain all other widgets and hold the stylesheet
        self.main_widget = QWidget(self)
        self._layout.addWidget(self.main_widget)

        # Remove margins
        self._layout.setContentsMargins(0, 0, 0, 0)

        # Set parent name
        name = f"Browser {self.tool_config.name}"
        self._parent.setWindowTitle(name)
        self._parent.setObjectName(name)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self.main_widget)
        self.tab_widget = QTabWidget(self)
        self.main_layout.addWidget(self.tab_widget)

        # Add tabs for each entity in the config
        for entity in self.tool_config.entities.values():
            tab = EntityTab(browser=self, entity=entity)
            self.tab_widget.addTab(tab, entity.label)

    def apply_stylesheet(self):
        stylesheet = get_stylesheet()
        self.main_widget.setStyleSheet(stylesheet)
        format_widgets(self.main_widget)

    @property
    def selected_tab(self) -> EntityTab:
        return self.tab_widget.currentWidget()  # type: ignore


if __name__ == "__main__":
    init_logging("browser")
    import sys

    from bluepepper.tools.browser.browser_example import config

    app = QApplication(sys.argv)
    dialog = QDialog()
    layout = QVBoxLayout(dialog)

    browser_widget = BrowserWidget(parent=dialog, tool_config=config)
    dialog.show()
    sys.exit(app.exec_())
