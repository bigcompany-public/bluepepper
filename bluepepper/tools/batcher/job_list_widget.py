from qtpy.QtWidgets import QListWidget, QSizePolicy


class JobListWidget(QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSpacing(1)
