"""
This module contains the LabWidget widget, used as a main page to display
and test every widget our tools use.
"""

from qtpy.QtWidgets import QMenu, QWidget

from bluepepper.gui.utils import stylesheet
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
    qtawesome,
)
from bluepepper.gui.widgets.lab_widget.ui_labwidget import Ui_LabWidget


class LabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui = Ui_LabWidget()
        ui.setupUi(self)

    def contextMenuEvent(self, event):
        """
        This method pops a Qmenu widget when the user right clicks on the table
        """
        menu = QMenu()
        menu.setStyleSheet(stylesheet)
        menu.addAction("Action1")
        menu.addAction("Action2 with a long name")
        action = menu.addAction("Action 3 with icon")
        icon = qtawesome.icon(
            "ei.adjust",
            scale_factor=1.1,
            color="#DDDDDD",
        )
        action.setIcon(icon)
        menu.exec_(event.globalPos())


if __name__ == "__main__":
    app = get_qt_app()
    widget = LabWidget()
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#1B6CD6")
    container = ContainerWidget(widget=widget, title="Lab", icon=icon)
    dialog = ContainerDialog(container)
    dialog.exec()
