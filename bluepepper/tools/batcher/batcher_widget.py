import qtawesome
from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from bluepepper.gui.utils import get_qta_icon, get_theme
from bluepepper.gui.widgets.container import ContainerDialog, ContainerWidget, format_widgets, get_qt_app
from bluepepper.tools.batcher.job_manager import JobManager
from bluepepper.tools.batcher.job_model import JobData, JobStatus
from bluepepper.tools.batcher.job_table_widget import JobTableItem, JobTableWidget
from bluepepper.tools.batcher.job_widget import JobWidget


class IconButton(QPushButton):
    def __init__(self, icon: QIcon):
        super().__init__()
        self.setIcon(icon)
        self.setProperty("status", "invisible")
        self.setFixedHeight(26)
        self.setFixedWidth(25)


class BatcherWidget(QWidget):
    """
    Main Batcher widget, intended to be embedded in the main BluePepper app

    Notes : kinda intricate way of managing the job widgets, since its inserting a widget into a list is kind of hacky
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.demo_widget_count = 1
        self._parent = parent

        # Icons for options expand
        theme = get_theme()
        i = 0.85
        self.icon_toggle_collapsed = qtawesome.icon("fa6s.caret-right", scale_factor=1.2, color=theme["icon_color"])
        self.icon_toggle_expanded = qtawesome.icon("fa6s.caret-down", scale_factor=1.2, color=theme["icon_color"])
        self.options_expanded = False

        self.attach_to_parent()
        self.job_table_widget = JobTableWidget(batcher=self)
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
        options_layout.setContentsMargins(3, 3, 3, 3)
        options_layout.setSpacing(3)

        # Options header
        options_header = QFrame()
        options_layout.addWidget(options_header)
        header_layout = QHBoxLayout(options_header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)
        self.button_expand_options = IconButton(self.icon_toggle_collapsed)
        header_layout.addWidget(self.button_expand_options)
        label = QLabel("Options")
        label.setProperty("tag", "H3")
        header_layout.addWidget(label)

        # Options content
        self.options_content_frame = QFrame()
        self.options_content_frame.setProperty("depth", 1)
        self.options_content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.options_content_frame.setHidden(True)  # Start collapsed
        options_layout.addWidget(self.options_content_frame)
        grid_layout = QGridLayout(self.options_content_frame)

        # Maximum threads
        max_threads_label = QLabel("Maximum Threads")
        grid_layout.addWidget(max_threads_label, 0, 0)
        self.spinbox_max_threads = QSpinBox()
        self.spinbox_max_threads.setRange(0, 100)
        self.spinbox_max_threads.setValue(3)
        grid_layout.addWidget(self.spinbox_max_threads, 0, 1)

        # Sorting options
        sort_label = QLabel("Sort by")
        grid_layout.addWidget(sort_label, 1, 0)
        self.cbb_sort = QComboBox()
        self.cbb_sort.addItems(["date", "name", "priority"])
        grid_layout.addWidget(self.cbb_sort, 1, 1)

        # Auto start
        label_auto_start = QLabel("Automatically start jobs")
        grid_layout.addWidget(label_auto_start, 0, 3)
        self.cb_auto_start = QCheckBox()
        self.cb_auto_start.setChecked(False)
        grid_layout.addWidget(self.cb_auto_start, 0, 4)

        # Delete finished jobs
        label_delete_finished = QLabel("Delete finished jobs")
        grid_layout.addWidget(label_delete_finished, 1, 3)
        self.cb_delete_finished = QCheckBox()
        self.cb_delete_finished.setChecked(False)
        grid_layout.addWidget(self.cb_delete_finished, 1, 4)

        # Mute notifications
        label_mute_success_notifications = QLabel("Mute Success Notifications")
        grid_layout.addWidget(label_mute_success_notifications, 0, 6)
        self.cb_mute_success_notifications = QCheckBox()
        self.cb_mute_success_notifications.setChecked(False)
        grid_layout.addWidget(self.cb_mute_success_notifications, 0, 7)

        label_mute_error_notifications = QLabel("Mute Error Notifications")
        grid_layout.addWidget(label_mute_error_notifications, 1, 6)
        self.cb_mute_error_notifications = QCheckBox()
        self.cb_mute_error_notifications.setChecked(False)
        grid_layout.addWidget(self.cb_mute_error_notifications, 1, 7)

        # Set column stretches to provide spacing and allow expansion
        grid_layout.setColumnStretch(2, 1)
        grid_layout.setColumnStretch(5, 1)

        # Job List
        job_list_frame = QFrame()
        job_list_frame.setProperty("depth", "0")
        main_layout.addWidget(job_list_frame)
        layout = QVBoxLayout(job_list_frame)
        layout.addWidget(self.job_table_widget)

        # Debug helpers
        self._button_demo_job = QPushButton("+ Add Demo Job")
        main_layout.addWidget(self._button_demo_job)
        self.button_sandbox = QPushButton("Sandbox")
        main_layout.addWidget(self.button_sandbox)

        # Widgets formatting
        format_widgets(self.main_widget)

    def _setup_signals(self):
        self._button_demo_job.clicked.connect(self._button_demo_job_clicked)
        self.button_sandbox.clicked.connect(self.button_sandbox_clicked)
        self.button_expand_options.clicked.connect(self.toggle_options_expand)
        self.cbb_sort.currentTextChanged.connect(self.on_sort_changed)

    def toggle_options_expand(self):
        if self.options_expanded:
            self.collapse_options()
        else:
            self.expand_options()
        self.options_expanded = not self.options_expanded

    def on_sort_changed(self) -> None:
        print("SORTING")
        self.job_table_widget.sortByColumn(0, Qt.DescendingOrder)

    def expand_options(self):
        self.button_expand_options.setIcon(self.icon_toggle_expanded)
        self.options_content_frame.setVisible(True)

    def collapse_options(self):
        self.button_expand_options.setIcon(self.icon_toggle_collapsed)
        self.options_content_frame.setVisible(False)

    def _button_demo_job_clicked(self):
        import json  # noqa: F401
        from pathlib import Path  # noqa: F401

        job_data = JobData(
            name=f"Test {self.demo_widget_count}",
            description="Just for testing purposes",
            script_path=Path(__file__).with_name("demo_script.py"),
            script_args=["--some_arg", json.dumps([{"hello": "world"}])],
            # module="bluepepper.tools.batcher.demo_script",
            # func="main",
            # kwargs={"some_arg": "LALALA"},
            notify_when_done=True,
            notify_message="",
        )
        self._add_job(job_data)
        self.demo_widget_count += 1

    def _add_job(self, job_data: JobData):
        # Create job widget
        item = JobTableItem()
        job_widget = JobWidget(job_data=job_data, batcher_widget=self, table_item=item)
        row_number = self.job_table_widget.rowCount()
        self.job_table_widget.insertRow(row_number)
        self.job_table_widget.setItem(row_number, self.job_table_widget._job_widget_column_index, item)
        self.job_table_widget.setCellWidget(row_number, 3, job_widget)

        # name item
        item = QTableWidgetItem()
        item.setText(job_data.name)
        self.job_table_widget.setItem(row_number, 0, item)

        # priority item
        item = QTableWidgetItem()
        item.setText(str(job_data.priority).zfill(3))
        self.job_table_widget.setItem(row_number, 1, item)

        # created at item
        item = QTableWidgetItem()
        item.setText(str(job_data.created_at))
        self.job_table_widget.setItem(row_number, 2, item)

    def add_script_job(
        self,
        name: str,
        description,
    ):
        job_data = JobData(name=name, description=description)

    @property
    def job_widgets(self) -> list[JobWidget]:
        return self.job_table_widget.job_widgets

    @property
    def sorted_job_widgets(self) -> list[JobWidget]:
        return self.job_table_widget.sorted_job_widgets

    @property
    def running_job_widgets(self) -> list[JobWidget]:
        return self.job_table_widget.running_job_widgets

    @property
    def running_job_widgets_count(self) -> int:
        return self.job_table_widget.running_job_widgets_count

    def button_sandbox_clicked(self):
        widgets = self.sorted_job_widgets
        for w in widgets:
            print(w.job_data.name, w.job_data.priority, w.job_data.created_at)

    @property
    def active_job_widgets(self) -> list[JobWidget]:
        """
        Returns the jobs that the batcher still has to process.
        This property is used when closing BluePepper, promptin the user if jobs are still active
        """
        active = [JobStatus.WAITING, JobStatus.RUNNING]
        return [job for job in self.job_widgets if job.job_data.status in active]


if __name__ == "__main__":
    app = get_qt_app()
    icon = get_qta_icon(name="mdi6.factory", scale_factor=1.25)
    widget = BatcherWidget()
    container = ContainerWidget(widget=widget, icon=icon, title="Batcher")
    dialog = ContainerDialog(container)
    dialog.exec()
