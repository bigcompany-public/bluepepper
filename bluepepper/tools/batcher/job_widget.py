from __future__ import annotations

from typing import TYPE_CHECKING

import qtawesome
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from bluepepper.gui.utils import format_widgets, get_theme

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.batcher.batcher_widget import BatcherWidget
    from bluepepper.tools.batcher.job_model import JobData


class JobWidget(QFrame):
    def __init__(self, job_data: JobData, batcher_widget: BatcherWidget):
        super().__init__()
        theme = get_theme()
        self.toggle_icon_collapsed = qtawesome.icon("fa6s.caret-right", scale_factor=1.2, color=theme["icon_color"])
        self.toggle_icon_expanded = qtawesome.icon("fa6s.caret-down", scale_factor=1.2, color=theme["icon_color"])

        self.job_data = job_data
        self.expanded = False
        self.setup_ui()
        self.setStyleSheet("")

    def setup_ui(self):
        # Add a container with a few pixels of margin to make the selection more visually clear in the JobListWidget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 0, 0, 0)

        main_frame = QFrame()
        main_frame.setProperty("depth", "4")
        layout.addWidget(main_frame)
        main_layout = QHBoxLayout(main_frame)

        # Expand toggle
        self.button_expand = QPushButton()
        self.button_expand.setFixedSize(20, 20)
        self.button_expand.setIcon(self.toggle_icon_collapsed)
        self.button_expand.setProperty("status", "invisible")
        self.button_expand.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_expand.clicked.connect(self.toggle_expand)
        main_layout.addWidget(self.button_expand)

        # Name
        label = QLabel(self.job_data.name)
        main_layout.addWidget(label)

        # Description
        label = QLabel(self.job_data.description)
        label.setProperty("status", "secondary")
        main_layout.addWidget(label)
        main_layout.addStretch()

        # Priority
        self.spinbox_priority = QSpinBox()
        self.spinbox_priority.setRange(1, 100)
        self.spinbox_priority.setValue(self.job_data.priority)
        self.spinbox_priority.setToolTip("Job priority (1 = low, 100 = high)")
        self.spinbox_priority.valueChanged.connect(self.on_priority_changed)
        main_layout.addWidget(self.spinbox_priority)

        # Widget formatting & adjustments
        format_widgets(self)
        self.spinbox_priority.setFixedWidth(50)

    def toggle_expand(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        self.button_expand.setIcon(self.toggle_icon_expanded)

    def collapse(self):
        self.button_expand.setIcon(self.toggle_icon_collapsed)

    def on_priority_changed(self, value: int):
        print(value)
