from __future__ import annotations

from typing import TYPE_CHECKING

import qtawesome
from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
)

from bluepepper.gui.utils import get_theme

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.batcher.batcher_widget import BatcherWidget
    from bluepepper.tools.batcher.job_model import JobData

SUBWIDGET_HEIGHT = 26


class IconButton(QPushButton):
    def __init__(self, icon: QIcon):
        super().__init__()
        self.setIcon(icon)
        self.setProperty("status", "invisible")
        self.setFixedHeight(SUBWIDGET_HEIGHT)
        self.setFixedWidth(25)


class JobWidget(QFrame):
    def __init__(self, job_data: JobData, batcher_widget: BatcherWidget, qlist_item: QListWidgetItem):
        super().__init__()
        self.job_data = job_data
        self.batchet_widget = batcher_widget
        self.qlist_item = qlist_item

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

        # Setup the widget
        self.setup_ui()

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
        self.button_expand.clicked.connect(self.toggle_expand)
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
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(self.job_data.progress)
        self.progress_bar.setFixedWidth(160)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        main_layout.addWidget(self.progress_bar)

        # Spacer
        spacer = QSpacerItem(20, 1)
        main_layout.addItem(spacer)

        # Priority
        self.spinbox_priority = QSpinBox()
        self.spinbox_priority.setRange(1, 100)
        self.spinbox_priority.setValue(self.job_data.priority)
        self.spinbox_priority.setToolTip("Job priority (1 = low, 100 = high)")
        self.spinbox_priority.valueChanged.connect(self.on_priority_changed)
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

    def toggle_expand(self):
        if self.expanded:
            self.collapse()
        else:
            self.expand()
        self.expanded = not self.expanded

    def expand(self):
        self.button_expand.setIcon(self.icon_toggle_expanded)
        self.expand_panel.setVisible(True)
        self.qlist_item.setSizeHint(self.sizeHint())

    def collapse(self):
        self.button_expand.setIcon(self.icon_toggle_collapsed)
        self.expand_panel.setHidden(True)
        self.qlist_item.setSizeHint(self.collapsed_size_hint)

    def on_priority_changed(self, value: int):
        print(value)
