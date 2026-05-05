from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import QEvent, Qt
from qtpy.QtWidgets import QAbstractItemView, QListWidget, QSizePolicy, QTableWidget, QTableWidgetItem

from bluepepper.tools.batcher.job_model import JobStatus

if TYPE_CHECKING:
    from bluepepper.tools.batcher.batcher_widget import BatcherWidget
    from bluepepper.tools.batcher.job_widget import JobWidget


class JobTableItem(QTableWidgetItem):
    """
    This object is only here to recover the row of the selected job widget
    JobWidgets have no row() method, so we need to find a workaround
    """

    def __init__(self):
        super().__init__()
        self.job_widget: JobWidget


class JobTableWidget(QTableWidget):
    def __init__(self, batcher: BatcherWidget) -> None:
        super().__init__(batcher)
        self._job_widget_column_index = 3
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumWidth(700)
        self.installEventFilter(self)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["name", "priority", "date", "job"])
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setColumnHidden(0, True)

    def get_job_widget_at_row(self, row: int) -> JobWidget:
        return self.cellWidget(row, column=self._job_widget_column_index)

    @property
    def job_widgets(self) -> list[JobWidget]:
        return [self.cellWidget(row, self._job_widget_column_index) for row in range(self.rowCount())]

    def cellWidget(self, row: int, column: int) -> JobWidget:
        """Fixes type annotation"""
        return super().cellWidget(row, column)  # type: ignore

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
    def running_job_widgets(self) -> list[JobWidget]:
        return [widget for widget in self.job_widgets if widget.job_data.status == JobStatus.RUNNING]

    @property
    def running_job_widgets_count(self) -> int:
        return len(self.running_job_widgets)

    @property
    def selected_rows(self) -> list[int]:
        return [item.row() for item in self.selectedIndexes() if item.column() == self._job_widget_column_index]

    def eventFilter(self, obj: JobTableWidget, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Delete:
                for item in obj.selectedItems():
                    item.job_widget.terminate_job()
                    obj.takeItem(obj.row(item))
                return True  # event consumed
        return super().eventFilter(obj, event)

    # def installEventFilter(self, filterObj: QObject) -> None:
    #     return super().installEventFilter(filterObj)
