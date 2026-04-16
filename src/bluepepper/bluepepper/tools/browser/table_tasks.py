from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from qtpy.QtWidgets import (
    QAbstractItemView,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
)

from bluepepper.tools.browser.browser_config import Task

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_config import Entity
    from bluepepper.tools.browser.browser_tab import EntityTab
    from bluepepper.tools.browser.browser_widget import BrowserWidget


class TableTasks(QTableWidget):
    """
    This class adds signals to the provided table widget
    This method was chosen over inheriting from QTableWidget and initializing a
    new widget to keep as much control as possible in QtDesigner
    """

    def __init__(self, tab: EntityTab):
        self.tab = tab
        self.browser: BrowserWidget = tab.browser
        self.entity: Entity = tab.entity
        self.document_table = self.tab.document_table
        super().__init__(tab)
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        self.setColumnCount(1)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        item = QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        self.setHorizontalHeaderLabels(["Tasks"])
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setHighlightSections(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setStretchLastSection(False)

    def setup_signals(self):
        """Sets ut the signals of the table widget"""
        self.itemSelectionChanged.connect(self.task_changed)

    def task_changed(self):
        """This method is triggered when the task's selection has changed"""
        task = self.get_selected_task()
        task_name = task.name if task else "None"
        logging.info(f"Task selection changed to {task_name}")
        self.tab.kind_table.update_items()

    def get_selected_item(self) -> TaskItem | None:
        items = self.selectedItems()
        if not items:
            return
        return items[0]

    def get_tasks(self) -> list[Task]:
        documents = self.document_table.selected_documents
        filtered_tasks = []
        for _, task in self.entity.tasks.items():
            if not task.doc_filter or not documents:
                filtered_tasks.append(task)
                continue
            filtered_documents = list(filter(task.filter, documents))
            if filtered_documents:
                filtered_tasks.append(task)

        return filtered_tasks

    def update_items(self):
        # Block signals to prevent unwanted updates
        self.blockSignals(True)

        # Store selection
        selected_task = self.get_selected_task()

        # Add items to the table
        self.clear_items()
        tasks = self.get_tasks()
        self.task_items = [TaskItem(task) for task in tasks]
        for item in self.task_items:
            row_number = self.rowCount()
            self.insertRow(row_number)
            self.setItem(row_number, 0, item)

            # Re-select task if it was selected before
            if selected_task:
                if item.task.name == selected_task.name:
                    item.setSelected(True)
                # else:
                #     self.tab.kind_table.update_items()

        # Re-enable signals
        self.blockSignals(False)

    def clear_items(self):
        self.clearContents()
        self.setRowCount(0)

    def get_selected_task(self) -> Task | None:
        item = self.get_selected_item()
        if not item:
            return
        return item.task


class TaskItem(QTableWidgetItem):
    """This class represents a task item within the TableTasks widget"""

    def __init__(self, task: Task = None):
        self.task = task
        super().__init__(self.task.label)
