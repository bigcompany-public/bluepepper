from pathlib import Path

from qtpy.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from bluepepper.gui.utils import get_qta_icon
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.tools.batcher.job_list_widget import JobListItem, JobListWidget
from bluepepper.tools.batcher.job_manager import JobManager
from bluepepper.tools.batcher.job_model import JobData
from bluepepper.tools.batcher.job_widget import JobWidget


class BatcherWidget(QWidget):
    """
    Main Batcher widget, intended to be embedded in the main BluePepper app

    Notes : kinda intricate way of managing the job widgets, since its inserting a widget into a list is kind of hacky
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.demo_widget_count = 1
        self._parent = parent
        self.attach_to_parent()
        self.job_list_widget = JobListWidget(batcher=self)
        self._setup_ui()
        self._setup_signals()
        self._manager = JobManager(batcher=self)
        self._manager.start_event_loop()

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
        self.setMinimumHeight(550)
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

        frame = QFrame()
        frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        options_layout.addWidget(frame)
        grid_layout = QGridLayout(frame)

        # Maximum threads
        max_threads_label = QLabel("Maximum Threads")
        grid_layout.addWidget(max_threads_label, 0, 0)
        self.spinbox_max_threads = QSpinBox()
        self.spinbox_max_threads.setRange(0, 100)
        self.spinbox_max_threads.setValue(3)
        grid_layout.addWidget(self.spinbox_max_threads, 0, 1)

        # Auto start
        label_auto_start = QLabel("Automatically start jobs")
        grid_layout.addWidget(label_auto_start, 1, 0)
        self.cb_auto_start = QCheckBox()
        self.cb_auto_start.setChecked(True)
        grid_layout.addWidget(self.cb_auto_start, 1, 1)

        # Delete finished jobs
        label_delete_finished = QLabel("Delete finished jobs")
        grid_layout.addWidget(label_delete_finished, 2, 0)
        self.cb_delete_finished = QCheckBox()
        self.cb_delete_finished.setChecked(True)
        grid_layout.addWidget(self.cb_delete_finished, 2, 1)

        # Job List
        job_list_frame = QFrame()
        job_list_frame.setProperty("depth", "0")
        main_layout.addWidget(job_list_frame)
        layout = QVBoxLayout(job_list_frame)
        layout.addWidget(self.job_list_widget)

        # Debug helpers
        self._button_demo_job = QPushButton("+ Add Demo Job")
        main_layout.addWidget(self._button_demo_job)
        self.button_sandbox = QPushButton("Sandbox")
        main_layout.addWidget(self.button_sandbox)

    def _setup_signals(self):
        self._button_demo_job.clicked.connect(self._button_demo_job_clicked)
        self.button_sandbox.clicked.connect(self.button_sandbox_clicked)

    def _button_demo_job_clicked(self):
        job_data = JobData(
            name=f"Test {self.demo_widget_count}",
            description="Just for testing purposes",
            script_path=Path(__file__).with_name("demo_script.py"),
        )
        self.add_job(job_data)
        self.demo_widget_count += 1

    def add_job(self, job_data: JobData):
        # Create job widget
        item = JobListItem()
        job_widget = JobWidget(job_data=job_data, batcher_widget=self, qlist_item=item)
        self.job_list_widget.addItem(item)
        self.job_list_widget.setItemWidget(item, job_widget)

    @property
    def job_widgets(self) -> list[JobWidget]:
        return self.job_list_widget.job_widgets

    @property
    def sorted_job_widgets(self) -> list[JobWidget]:
        return self.job_list_widget.sorted_job_widgets

    @property
    def running_job_widgets(self) -> list[JobWidget]:
        return self.job_list_widget.running_job_widgets

    @property
    def running_job_widgets_count(self) -> int:
        return self.job_list_widget.running_job_widgets_count

    def button_sandbox_clicked(self):
        widgets = self.sorted_job_widgets
        for w in widgets:
            print(w.job_data.name, w.job_data.priority, w.job_data.created_at)


if __name__ == "__main__":
    app = get_qt_app()
    icon = get_qta_icon(name="mdi6.factory", scale_factor=1.25)
    widget = BatcherWidget()
    container = ContainerWidget(widget=widget, icon=icon, title="Batcher")
    dialog = ContainerDialog(container)
    dialog.exec()
