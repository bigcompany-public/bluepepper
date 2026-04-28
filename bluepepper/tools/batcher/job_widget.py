from __future__ import annotations

import math
from datetime import datetime
from typing import TYPE_CHECKING

import qtawesome
from qtpy.QtCore import QSize, QTimer
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
)

from bluepepper.gui.utils import get_theme, stylesheet
from bluepepper.tools.batcher.job_model import JobData, JobStatus
from bluepepper.tools.batcher.job_thread import JobThread

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.batcher.batcher_widget import BatcherWidget, JobListItem

SUBWIDGET_HEIGHT = 26


class IconButton(QPushButton):
    def __init__(self, icon: QIcon):
        super().__init__()
        self.setIcon(icon)
        self.setProperty("status", "invisible")
        self.setFixedHeight(SUBWIDGET_HEIGHT)
        self.setFixedWidth(25)


class ProgressBar(QProgressBar):
    def __init__(self, job_widget: JobWidget):
        super().__init__()
        self.job_widget = job_widget
        self.setRange(0, 100)
        self.setValue(0)
        self.setFixedWidth(160)
        self.setFixedHeight(20)
        self.setTextVisible(True)
        self.redraw()

    def redraw(self):
        status = self.job_widget.job_data.status.value
        self.setFormat(status.capitalize())
        self.setProperty("status", status)  # The property drives the stylesheet

        # Re-apply stylesheet to force a redraw
        self.setStyleSheet(stylesheet)

    def update_progress(self, value: int) -> None:
        value = int(value)
        margin = 7

        # progress bar value and actual value differ,
        # because the rounded borders cause issue with small values
        if value >= 100:
            visual_value = 100
        elif value <= 0 and self.job_widget.job_data.status != JobStatus.RUNNING:
            visual_value = 0
        else:
            number_of_parts = 100 - margin * 2
            part = number_of_parts / 100
            visual_value = margin + (part * value)
            visual_value = math.ceil(visual_value)

        self.setFormat(f"{str(value)}%")
        self.setValue(visual_value)


class JobWidget(QFrame):
    def __init__(self, job_data: JobData, batcher_widget: BatcherWidget, qlist_item: JobListItem):
        super().__init__()
        self.job_data = job_data
        self.batchet_widget = batcher_widget
        self.job_list_widget = self.batchet_widget.job_list_widget
        self.qlist_item = qlist_item

        # Insert self into the item
        self.qlist_item.job_widget = self

        # Icons
        theme = get_theme()
        i = 0.85
        self.icon_toggle_collapsed = qtawesome.icon("fa6s.caret-right", scale_factor=1.2, color=theme["icon_color"])
        self.icon_toggle_expanded = qtawesome.icon("fa6s.caret-down", scale_factor=1.2, color=theme["icon_color"])
        self.icon_start = qtawesome.icon("fa5s.play", scale_factor=0.75 * i, color=theme["icon_color"])
        self.icon_stop = qtawesome.icon("fa5s.stop", scale_factor=0.9 * i, color=theme["icon_color"])
        self.icon_restart = qtawesome.icon("fa5s.undo-alt", scale_factor=0.9 * i, color=theme["icon_color"])
        self.icon_delete = qtawesome.icon("fa5s.trash-alt", scale_factor=1 * i, color=theme["icon_color"])

        # Attributes for internal working
        self.expanded = False
        self.collapsed_size_hint: QSize

        # Internal timer for runtime
        self._runtime_timer = QTimer(self)
        self._runtime_timer.setInterval(1000)
        self._runtime_timer.timeout.connect(self.update_runtime)

        # Setup the widget
        self.setup_ui()
        self.setup_signals()

        # Create thread
        self._thread = JobThread(job_widget=self)

    def setup_ui(self):
        # Add a container with a few pixels of margin to make the selection more visually clear in the JobListWidget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 0, 0, 0)

        # Layout with the "main frame" and the frame that appears when expanded
        container_frame = QFrame()
        container_frame.setProperty("depth", "4")
        layout.addWidget(container_frame)
        container_layout = QVBoxLayout(container_frame)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Main frame with the main job display
        main_frame = QFrame()
        container_layout.addWidget(main_frame)
        main_layout = QHBoxLayout(main_frame)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(3)

        # Expand toggle
        self.button_expand = IconButton(self.icon_toggle_collapsed)
        main_layout.addWidget(self.button_expand)

        # Name
        label = QLabel(self.job_data.name)
        main_layout.addWidget(label)

        # Spacer
        spacer = QSpacerItem(6, 1)
        main_layout.addItem(spacer)

        # Description
        label = QLabel(self.job_data.description)
        label.setProperty("status", "secondary")
        main_layout.addWidget(label)
        main_layout.addStretch()

        # Progress bar
        self.progress_bar = ProgressBar(self)
        main_layout.addWidget(self.progress_bar)

        # Spacer
        spacer = QSpacerItem(20, 1)
        main_layout.addItem(spacer)

        # Priority
        self.spinbox_priority = QSpinBox()
        self.spinbox_priority.setRange(1, 100)
        self.spinbox_priority.setValue(self.job_data.priority)
        self.spinbox_priority.setToolTip("Job priority (1 = low, 100 = high)")
        self.spinbox_priority.setFixedWidth(50)
        main_layout.addWidget(self.spinbox_priority)

        # Start button
        self.button_start = IconButton(self.icon_start)
        main_layout.addWidget(self.button_start)

        # Stop button
        self.button_stop = IconButton(self.icon_stop)
        main_layout.addWidget(self.button_stop)

        # Restart button
        self.button_restart = IconButton(self.icon_restart)
        main_layout.addWidget(self.button_restart)

        # Delete button
        self.button_delete = IconButton(self.icon_delete)
        main_layout.addWidget(self.button_delete)

        # Store size hint without the expanded frame
        self.collapsed_size_hint = self.sizeHint()
        # The size hint is slightly off, maybe because of layout margins
        self.collapsed_size_hint.setHeight(self.collapsed_size_hint.height() + 2)
        self.qlist_item.setSizeHint(self.collapsed_size_hint)

        # Expanded panel
        self.expand_panel = QFrame()
        container_layout.addWidget(self.expand_panel)

        # Layout to slightly move the panel to the right
        layout = QHBoxLayout(self.expand_panel)
        layout.setContentsMargins(0, 2, 2, 2)
        spacer = QSpacerItem(16, 1)
        layout.addItem(spacer)

        sub_expand_panel = QFrame()
        layout.addWidget(sub_expand_panel)
        sub_expand_layout = QVBoxLayout(sub_expand_panel)
        sub_expand_layout.setContentsMargins(0, 0, 0, 0)

        # Set original visibility
        self.expand_panel.setHidden(True)

        # Runtime
        self.label_runtime = QLabel("Runtime: Not started yet")
        sub_expand_layout.addWidget(self.label_runtime)

        # Stdout
        self.stdout_view = QPlainTextEdit()
        self.stdout_view.setProperty("status", "code")
        self.stdout_view.setReadOnly(True)
        self.stdout_view.setFixedHeight(200)
        sub_expand_layout.addWidget(self.stdout_view)
        self.stdout_view.setPlainText("this is\na multiple line\ntext\n" * 30)

    def setup_signals(self):
        self.button_expand.clicked.connect(self.toggle_expand)
        self.spinbox_priority.valueChanged.connect(self.on_priority_changed)
        self.button_start.clicked.connect(self.on_button_start_clicked)
        self.button_stop.clicked.connect(self.on_button_stop_clicked)
        self.button_restart.clicked.connect(self.on_button_restart_clicked)
        self.button_delete.clicked.connect(self.on_button_delete_clicked)

    def toggle_expand(self):
        to_do = "collapse" if self.expanded else "expand"
        selection = self.job_list_widget.selectedItems()
        if not self.qlist_item in selection:
            self.job_list_widget.clearSelection()
            self.qlist_item.setSelected(True)
        
        for item in self.batchet_widget.job_list_widget.selectedItems():
            if to_do == "collapse":
                item.job_widget.collapse()
            else:
                item.job_widget.expand()
            item.job_widget.expanded = not item.job_widget.expanded

    def expand(self):
        self.button_expand.setIcon(self.icon_toggle_expanded)
        self.expand_panel.setVisible(True)
        self.qlist_item.setSizeHint(self.sizeHint())

    def collapse(self):
        print("collpase triggered")
        self.button_expand.setIcon(self.icon_toggle_collapsed)
        self.expand_panel.setHidden(True)
        self.qlist_item.setSizeHint(self.collapsed_size_hint)

    def on_priority_changed(self, value: int):
        selection = self.job_list_widget.selectedItems()
        if not self.qlist_item in selection:
            self.job_list_widget.clearSelection()
            self.qlist_item.setSelected(True)
        
        for item in self.batchet_widget.job_list_widget.selectedItems():
            item.job_widget.spinbox_priority.blockSignals(True)
            item.job_widget.spinbox_priority.setValue(value)
            item.job_widget.job_data.priority = value
            item.job_widget.spinbox_priority.blockSignals(False)


    def on_button_start_clicked(self):
        selection = self.job_list_widget.selectedItems()
        if not self.qlist_item in selection:
            self.job_list_widget.clearSelection()
            self.qlist_item.setSelected(True)
        
        for item in self.batchet_widget.job_list_widget.selectedItems():
            item.job_widget.progress_bar.update_progress(0)
            item.job_widget.set_status(JobStatus.WAITING)

    def on_button_restart_clicked(self):
        selection = self.job_list_widget.selectedItems()
        if not self.qlist_item in selection:
            self.job_list_widget.clearSelection()
            self.qlist_item.setSelected(True)
        
        for item in self.batchet_widget.job_list_widget.selectedItems():
            item.job_widget.terminate_job()
            item.job_widget.progress_bar.update_progress(0)
            item.job_widget.set_status(JobStatus.WAITING)

    def on_button_delete_clicked(self):
        selection = self.job_list_widget.selectedItems()
        if not self.qlist_item in selection:
            self.job_list_widget.clearSelection()
            self.qlist_item.setSelected(True)
        
        for item in self.batchet_widget.job_list_widget.selectedItems():
            item.job_widget.delete_job()

    def delete_job(self):
        self.terminate_job()
        row = self.batchet_widget.job_list_widget.row(self.qlist_item)
        self.batchet_widget.job_list_widget.takeItem(row)

    def on_button_stop_clicked(self):
        selection = self.job_list_widget.selectedItems()
        if not self.qlist_item in selection:
            self.job_list_widget.clearSelection()
            self.qlist_item.setSelected(True)
        
        for item in self.batchet_widget.job_list_widget.selectedItems():
            if item.job_widget.job_data.status == JobStatus.RUNNING:
                item.job_widget.terminate_job_from_user()
            if item.job_widget.job_data.status == JobStatus.WAITING:
                item.job_widget.suspend_job()


    def start(self):
        # Do nothing if the job is already running
        if self.job_data.status == JobStatus.RUNNING:
            return

        self.job_data.status = JobStatus.RUNNING
        self._start_time = datetime.now()
        self.reset_stdout()

        # Start timer
        self._runtime_secs = 0
        self.update_runtime()
        self._runtime_timer.start()

        # Start Thread
        self._thread.start()

        # Update Progress bar
        self.progress_bar.redraw()
        self.progress_bar.update_progress(0)

    def reset_stdout(self) -> None:
        self.stdout_view.clear()

    def update_runtime(self) -> None:
        h = self._runtime_secs // 3600
        m = (self._runtime_secs % 3600) // 60
        s = self._runtime_secs % 60
        self.label_runtime.setText(f"Runtime: {h:02d}:{m:02d}:{s:02d}")
        self._runtime_secs += 1

    def update_log(self, line: str) -> None:
        self.stdout_view.appendPlainText(line)

    def job_finished(self):
        self.stdout_view.appendPlainText("Batcher job finished successfully")
        self.set_status(JobStatus.FINISHED)
        self.progress_bar.update_progress(100)
        if self.batchet_widget.cb_delete_finished.isChecked():
            self.delete_job()

    def terminate_job_from_script(self):
        self.stdout_view.appendPlainText("Batcher job terminated from within the script")
        self.terminate_job()

    def terminate_job_from_user(self):
        self.stdout_view.appendPlainText("Batcher job terminated by the user")
        self.terminate_job()

    def terminate_job(self):
        self._thread.terminate()
        self.set_status(JobStatus.TERMINATED)

    def suspend_job(self):
        self._thread.terminate()
        self.set_status(JobStatus.SUSPENDED)

    def error_encountered(self):
        self.stdout_view.appendPlainText("Batcher job encountered an error")
        self.set_status(JobStatus.ERROR)

    def set_status(self, status: JobStatus) -> None:
        if status != JobStatus.RUNNING:
            self._runtime_timer.stop()
        self.job_data.status = status
        self.progress_bar.redraw()
