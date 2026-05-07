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
        self._columns = ["name", "priority", "date", "status", "job"]
        self._name_column_index = self._columns.index("name")
        self._priority_column_index = self._columns.index("priority")
        self._date_column_index = self._columns.index("date")
        self._status_column_index = self._columns.index("status")
        self._job_column_index = self._columns.index("job")
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumWidth(700)
        self.installEventFilter(self)
        self.setColumnCount(len(self._columns))
        self.setHorizontalHeaderLabels(self._columns)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        for i in range(len(self._columns) - 1):
            self.setColumnHidden(i, True)

    def get_job_widget_at_row(self, row: int) -> JobWidget:
        return self.cellWidget(row, column=self._job_column_index)

    @property
    def job_widgets(self) -> list[JobWidget]:
        return [self.cellWidget(row, self._job_column_index) for row in range(self.rowCount())]

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
        return [item.row() for item in self.selectedIndexes() if item.column() == self._job_column_index]

    @property
    def selected_job_widgets(self) -> list[JobWidget]:
        return [self.get_job_widget_at_row(row) for row in self.selected_rows]

    def eventFilter(self, table_widget: JobTableWidget, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Delete:
                self.delete_selected_jobs()
                return True  # event consumed
        return super().eventFilter(table_widget, event)

    def delete_selected_jobs(self):
        rows_to_remove = []
        for row in self.selected_rows:
            job_widget = self.get_job_widget_at_row(row)
            job_widget.terminate_job()
            rows_to_remove.append(row)
        for row in reversed(rows_to_remove):
            self.removeRow(row)
