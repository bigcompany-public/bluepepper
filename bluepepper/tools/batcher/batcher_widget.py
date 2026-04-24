from pathlib import Path

from qtpy.QtWidgets import QFrame, QLabel, QListWidgetItem, QPushButton, QVBoxLayout, QWidget

from bluepepper.gui.utils import get_qta_icon
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.tools.batcher.job_list_widget import JobListWidget
from bluepepper.tools.batcher.job_model import JobData
from bluepepper.tools.batcher.job_widget import JobWidget


class BatcherWidget(QWidget):
    """
    Main Batcher widget, intended to be embedded in the main BluePepper app
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._parent = parent
        self.attach_to_parent()
        self.job_list_widget = JobListWidget(self)
        self._job_counter = 0
        self._setup_ui()
        self._setup_signals()

    def attach_to_parent(self):
        self._layout: QVBoxLayout
        if not self._parent:
            self._layout = QVBoxLayout()
            self.setLayout(self._layout)
        elif not self._parent.layout():
            self._layout = QVBoxLayout()
            self._parent.setLayout(self._layout)
        else:
            self._layout = self._parent.layout()  # type: ignore

        # Create main widget, who will contain all other widgets and hold the stylesheet
        self.main_widget = QWidget(self)
        self._layout.addWidget(self.main_widget)

        # Remove margins
        self._layout.setContentsMargins(0, 0, 0, 0)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self.main_widget)
        label_title = QLabel("Batcher")
        label_title.setProperty("tag", "H2")
        main_layout.addWidget(label_title)

        # Global options
        options_frame = QFrame()
        options_frame.setProperty("depth", "0")
        main_layout.addWidget(options_frame)

        options_layout = QVBoxLayout(options_frame)
        label = QLabel("Options")
        label.setProperty("tag", "H3")
        options_layout.addWidget(label)

        # Job List
        job_list_frame = QFrame()
        job_list_frame.setProperty("depth", "0")
        main_layout.addWidget(job_list_frame)
        layout = QVBoxLayout(job_list_frame)
        layout.addWidget(self.job_list_widget)

        # Debug helpers
        self._button_demo_job = QPushButton("+ Add Demo Job")
        main_layout.addWidget(self._button_demo_job)

    def _setup_signals(self):
        self._button_demo_job.clicked.connect(self._button_domo_job_clicked)

    def _button_domo_job_clicked(self):
        job_data = JobData(
            name="Test", description="Just for testing purposes", script_path=Path(__file__).with_name("demo_script.py")
        )
        self.add_job(job_data)

    def add_job(self, job_data: JobData):
        item = QListWidgetItem()
        job_widget = JobWidget(job_data=job_data, batcher_widget=self, qlist_item=item)
        self.job_list_widget.addItem(item)
        self.job_list_widget.setItemWidget(item, job_widget)


if __name__ == "__main__":
    app = get_qt_app()
    icon = get_qta_icon(name="mdi6.factory", scale_factor=1.25)
    widget = BatcherWidget()
    container = ContainerWidget(widget=widget, icon=icon, title="Batcher")
    dialog = ContainerDialog(container)
    dialog.exec()
