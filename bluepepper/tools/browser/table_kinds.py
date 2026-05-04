from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from qtpy.QtCore import QEvent, Qt
from qtpy.QtWidgets import (
    QAbstractItemView,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
)

from bluepepper.core import database
from bluepepper.tools.browser.browser_config import FileKind, MenuAction
from bluepepper.tools.browser.browser_menu import BrowserMenu

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_config import Entity, MenuAction
    from bluepepper.tools.browser.browser_tab import EntityTab
    from bluepepper.tools.browser.browser_widget import BrowserWidget


class TableFileKinds(QTableWidget):
    """
    This class adds signals to the provided table widget
    This method was chosen over inheriting from QTableWidget and initializing a
    new widget to keep as much control as possible in QtDesigner
    """

    def __init__(self, tab: EntityTab):
        self.tab = tab
        self.browser: BrowserWidget = tab.browser
        self.entity: Entity = tab.entity
        self.collection = database.db.get_collection(self.entity.collection)
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
        self.setHorizontalHeaderLabels(["FileKinds"])
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
        self.itemSelectionChanged.connect(self.kind_changed)

    def kind_changed(self):
        """This method is triggered when the kind's selection has changed"""
        kind_names = [item.kind.name for item in self.get_selected_items()]
        logging.info(f"FileKind selection changed to {kind_names}")
        self.tab.file_table.update_items()

    def get_selected_items(self) -> list[FileKindItem]:
        return self.selectedItems()

    def get_selected_kind(self) -> FileKind | None:
        selected = self.get_selected_items()
        if selected:
            return selected[0].kind

    def get_kinds(self) -> list[FileKind]:
        task = self.tab.task_table.get_selected_task()
        if not task:
            return []
        return list(task.kinds.values())

    def update_items(self):
        self.clear_items()
        kinds = self.get_kinds()
        self.kind_items = [FileKindItem(kind) for kind in kinds]
        if not self.kind_items:
            self.kind_items = [FileKindItem(None)]

        # Add items to the table
        for item in self.kind_items:
            row_number = self.rowCount()
            self.insertRow(row_number)
            self.setItem(row_number, 0, item)

    def clear_items(self):
        self.clearContents()
        self.setRowCount(0)

    @property
    def selected_kind(self) -> FileKind | None:
        items = self.selectedItems() or []
        items = [item for item in items if isinstance(item, FileKindItem)]
        kinds = [item.kind for item in items]
        if kinds:
            return kinds[0]

    def contextMenuEvent(self, event: QEvent):
        """
        This method pops a Qmenu widget when the user right clicks on the table
        """
        if not self.entity.document_actions:
            return
        menu = TableFileKindsMenu(tab=self.tab, kind=self.selected_kind, event=event)
        menu.exec_(event.globalPos())


class FileKindItem(QTableWidgetItem):
    """This class represents a kind item within the TableFileKinds widget"""

    def __init__(self, kind: FileKind = None):
        self.kind = kind
        super().__init__("")
        self.set_label()
        self.set_enabled()

    def set_label(self):
        self.setText(self.kind.label if self.kind else "Select a task")

    def set_enabled(self):
        if not self.kind:
            self.setFlags(self.flags() ^ Qt.ItemFlag.ItemIsEnabled)


class TableFileKindsMenu(BrowserMenu):
    def __init__(self, tab: EntityTab, kind: FileKind, event: QEvent):
        actions = kind.kind_actions if kind else []
        targets = tab.document_table.selected_documents
        super().__init__(tab, event, actions=actions, targets=targets, kind=kind)
