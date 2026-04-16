"""
This module contains the LabWidget widget, used as a main page to display
and test every widget our tools use.
"""

from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
    qtawesome,
)
from bluepepper.gui.widgets.lab_widget.ui_labwidget import Ui_LabWidget
from qtpy.QtWidgets import QWidget


class LabWidget(QWidget):
    def __init__(self):
        super().__init__()
        ui = Ui_LabWidget()
        ui.setupUi(self)


if __name__ == "__main__":
    app = get_qt_app()
    widget = LabWidget()
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#1B6CD6")
    container = ContainerWidget(widget=widget, title="Lab", icon=icon)
    dialog = ContainerDialog(container)
    dialog.exec()
