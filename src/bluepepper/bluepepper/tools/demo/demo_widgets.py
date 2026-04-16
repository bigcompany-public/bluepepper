"""
These are example widgets that implement BluePepperWidget to handle the stylesheet
Two methods are on display here : one that
"""

import qtawesome
from bluepepper.gui.utils import get_qt_app
from bluepepper.gui.widgets.container import ContainerDialog, ContainerWidget
from bluepepper.tools.demo.ui_demo_widget import Ui_demo
from qtpy.QtWidgets import QLabel, QVBoxLayout, QWidget


class DemoWidgetQtDesigner(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        ui = Ui_demo()
        ui.setupUi(self)

    def do_stuff(self):
        print("Hello World")


class DemoWidgetPythonCode(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Hello World"))

    def do_stuff(self):
        print("Hello World")


def show_dialog_qtdesigner():
    app = get_qt_app()  # noqa: F841
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#45AB9E")
    widget = DemoWidgetQtDesigner()
    container = ContainerWidget(widget=widget, title="DemoQtDesigner", icon=icon)
    dialog = ContainerDialog(container=container)
    widget.do_stuff()
    dialog.exec()


def show_dialog_pythonic():
    app = get_qt_app()  # noqa: F841
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#45AB9E")

    widget = DemoWidgetPythonCode()
    container = ContainerWidget(widget=widget, title="DemoPythonCode", icon=icon)
    dialog = ContainerDialog(container=container)
    dialog.exec()


def show_widget():
    app = get_qt_app()  # noqa: F841
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#45AB9E")

    widget = DemoWidgetPythonCode()
    container = ContainerWidget(widget=widget, title="DemoStandaloneWidget", icon=icon)
    container.show()
    app.exec()


def insert_widget_in_another_widget():
    app = get_qt_app()
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#45AB9E")

    # Placeholder parent widget
    parent_widget = QWidget()
    layout = QVBoxLayout()
    parent_widget.setLayout(layout)
    layout.addWidget(QLabel("Adding subwidget"))

    # Your widget
    child_widget = DemoWidgetQtDesigner()
    layout.addWidget(child_widget)

    # Add the parent widget to the container
    container = ContainerWidget(
        widget=parent_widget, title="DemoInsertedWidget", icon=icon
    )
    container.show()
    child_widget.do_stuff()
    parent_widget.show()
    app.exec()


if __name__ == "__main__":
    app = get_qt_app()
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#45AB9E")

    # show_dialog_qtdesigner()
    # show_dialog_pythonic()
    # show_widget()
    insert_widget_in_another_widget()
