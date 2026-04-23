from qtpy.QtWidgets import QFrame, QLabel, QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from bluepepper.gui.utils import get_qta_icon
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.tools.batcher.job_list_widget import JobListWidget
from bluepepper.tools.batcher.job_widget import JobWidget


class BatcherWidget(QWidget):
    """
    Main Batcher widget, intended to be embedded in the main BluePepper app
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.job_list_widget = JobListWidget(self)
        # self._manager = JobManager(self)
        self._job_counter = 0
        self._setup_ui()
        self._setup_signals()
        # self._connect_manager()

    def _setup_ui(self):
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        main_layout = QVBoxLayout(self)
        label_title = QLabel("Batcher")
        label_title.setProperty("tag", "H2")
        main_layout.addWidget(label_title)

        # Global options
        options_frame = QFrame()
        options_frame.setProperty("depth", "0")
        options_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout.addWidget(options_frame)

        options_layout = QVBoxLayout(options_frame)
        label = QLabel("Options")
        label.setProperty("tag", "H3")
        options_layout.addWidget(label)

        # Job List
        job_list_frame = QFrame()
        job_list_frame.setProperty("depth", "0")
        job_list_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(job_list_frame)
        layout = QVBoxLayout(job_list_frame)
        layout.addWidget(self.job_list_widget)

        # Debug helpers
        self._button_demo_job = QPushButton("+ Add Demo Job")
        self._button_demo_job.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addWidget(self._button_demo_job)

    def _setup_signals(self):
        self._button_demo_job.clicked.connect(self._button_domo_job_clicked)

    def _button_domo_job_clicked(self):
        print(self.job_list_widget.selectedItems())

        item = QListWidgetItem()
        job_widget = JobWidget()
        self.job_list_widget.addItem(item)
        self.job_list_widget.setItemWidget(item, job_widget)
        item.setSizeHint(job_widget.sizeHint())


if __name__ == "__main__":
    app = get_qt_app()
    icon = get_qta_icon(name="mdi6.factory", scale_factor=1.25)
    widget = BatcherWidget()
    container = ContainerWidget(widget=widget, icon=icon, title="Batcher")
    dialog = ContainerDialog(container)
    dialog.exec()
