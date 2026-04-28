from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QListWidget, QListWidgetItem, QSizePolicy

from bluepepper.tools.batcher.job_model import JobStatus

if TYPE_CHECKING:
    from bluepepper.tools.batcher.batcher_widget import BatcherWidget
    from bluepepper.tools.batcher.job_widget import JobWidget


class JobListItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
        self.job_widget: JobWidget


class JobListWidget(QListWidget):
    def __init__(self, batcher: BatcherWidget) -> None:
        super().__init__(batcher)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSpacing(1)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumWidth(700)

    @property
    def job_widgets(self) -> list[JobWidget]:
        return [item.job_widget for item in self.job_items]

    @property
    def sorted_job_widgets(self) -> list[JobWidget]:
        """
        Sort job, first by priority, then by creation time, meaning that at equal priority, the jobs will be treated
        first in, first out
        """
        widgets = self.job_widgets
        sorted_widgets = sorted(
            widgets,
            key=lambda job_widget: (-job_widget.job_data.priority, job_widget.job_data.created_at),
        )
        return sorted_widgets

    @property
    def job_items(self) -> list[JobListItem]:
        return self.findItems("*", Qt.MatchFlag.MatchWildcard)  # type: ignore

    @property
    def running_job_widgets(self) -> list[JobWidget]:
        return [widget for widget in self.job_widgets if widget.job_data.status == JobStatus.RUNNING]

    @property
    def running_job_widgets_count(self) -> int:
        return len(self.running_job_widgets)
    
    def selectedItems(self) -> list[JobListItem]:
        return super().selectedItems() # type: ignore
