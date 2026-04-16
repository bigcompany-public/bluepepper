import qtawesome
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bluepepper.gui.widgets.container import ContainerWidget


class MyLineEditWidget(QWidget):
    def __init__(self, parent=None):
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


# --- Launch ---

app = QApplication.instance() or QApplication(["blender"])

user_widget = MyLineEditWidget()
icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#000000")
container = ContainerWidget(user_widget, title="Enter Name", icon=icon)
container.confirmed.connect(lambda value: print(f"Confirmed: {value!r}"))
user_widget.ok_button.clicked.connect(
    lambda: container._confirm(user_widget.line_edit.text())
)

container.show()
