from __future__ import annotations

import importlib
import logging
from functools import partial
from typing import TYPE_CHECKING

import qtawesome
from qtpy.QtCore import QEvent, Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QAbstractItemView,
    QMenu,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
)

from bluepepper.core import database
from bluepepper.gui.utils import get_icon
from bluepepper.tools.browser.browser_config import Kind

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_config import Entity, MenuAction
    from bluepepper.tools.browser.browser_tab import EntityTab
    from bluepepper.tools.browser.browser_widget import BrowserWidget


class TableKinds(QTableWidget):
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
        self.setHorizontalHeaderLabels(["Kinds"])
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
        logging.info(f"Kind selection changed to {kind_names}")
        self.tab.file_table.update_items()

    def get_selected_items(self) -> list[KindItem]:
        return self.selectedItems()

    def get_selected_kind(self) -> Kind | None:
        selected = self.get_selected_items()
        if selected:
            return selected[0].kind

    def get_kinds(self) -> list[Kind]:
        task = self.tab.task_table.get_selected_task()
        if not task:
            return []
        return list(task.kinds.values())

    def update_items(self):
        self.clear_items()
        kinds = self.get_kinds()
        self.kind_items = [KindItem(kind) for kind in kinds]
        if not self.kind_items:
            self.kind_items = [KindItem(None)]

        # Add items to the table
        for item in self.kind_items:
            row_number = self.rowCount()
            self.insertRow(row_number)
            self.setItem(row_number, 0, item)

    def clear_items(self):
        self.clearContents()
        self.setRowCount(0)

    @property
    def selected_kind(self) -> Kind | None:
        items = self.selectedItems() or []
        items = [item for item in items if isinstance(item, KindItem)]
        kinds = [item.kind for item in items]
        if kinds:
            return kinds[0]

    def contextMenuEvent(self, event: QEvent):
        """
        This method pops a Qmenu widget when the user right clicks on the table
        """
        if not self.entity.document_actions:
            return
        menu = TableKindsMenu(tab=self.tab, kind=self.selected_kind, event=event)
        menu.exec_(event.globalPos())


class KindItem(QTableWidgetItem):
    """This class represents a kind item within the TableKinds widget"""

    def __init__(self, kind: Kind = None):
        self.kind = kind
        super().__init__("")
        self.set_label()
        self.set_enabled()

    def set_label(self):
        self.setText(self.kind.label if self.kind else "Select a task")

    def set_enabled(self):
        if not self.kind:
            self.setFlags(self.flags() ^ Qt.ItemFlag.ItemIsEnabled)


class TableKindsMenu(QMenu):
    def __init__(self, tab: EntityTab, kind: Kind, event: QEvent):
        super().__init__(tab)
        self.tab = tab
        self.kind = kind
        self._event = event
        self.entity = self.tab.entity
        self.register_actions()

    def register_actions(self):
        for action in self.get_actions_to_register():
            self.register_action(action)

    def get_actions_to_register(self):
        # Only register action if the selected documents respect the filter
        documents = self.tab.document_table.selected_documents
        filtered_actions = []
        for action in self.kind.kind_actions:
            if not action.doc_filter:
                filtered_actions.append(action)
                continue
            filtered_documents = list(filter(action.doc_filter, documents))
            if filtered_documents:
                filtered_actions.append(action)

        return filtered_actions

    def register_action(self, menu_action: MenuAction):
        action = self.addAction(menu_action.label)

        # Set icon
        icon = None
        if menu_action.icon:
            icon = QIcon(get_icon(menu_action.icon).as_posix())
        elif menu_action.qta_icon:
            icon = qtawesome.icon(
                menu_action.qta_icon, scale_factor=1.1, color=menu_action.qta_icon_color
            )

        if icon:
            action.setIcon(icon)

        # Import the module and get the callable
        module = importlib.import_module(menu_action.module)
        func = getattr(module, menu_action.callable)

        def execute_on_all_documents():
            # Filter documents
            documents = self.tab.document_table.selected_documents
            if menu_action.doc_filter:
                documents = list(filter(menu_action.doc_filter, documents))

            # Conform kwargs
            kwargs = {}
            for key, value in menu_action.kwargs.items():
                kwargs[key] = value
                if value == "<documents>":
                    kwargs[key] = documents
                elif value == "<document_names>":
                    kwargs[key] = [doc[self.entity.name] for doc in documents]
                elif value == "<document_ids>":
                    kwargs[key] = [doc["_id"] for doc in documents]
                elif value == "<browser>":
                    kwargs[key] = self.tab.browser
                elif value == "<convention>":
                    kwargs[key] = self.kind.convention

            # Execute callback with provided kwargs
            callback = partial(func, **kwargs)
            callback()

        # Create a wrapper that calls the function for each selected document
        def execute_on_each_document():
            documents = self.tab.document_table.selected_documents
            if menu_action.doc_filter:
                documents = list(filter(menu_action.doc_filter, documents))

            for document in documents:
                # Format kwargs
                kwargs = {}
                for key, value in menu_action.kwargs.items():
                    kwargs[key] = value
                    if value == "<document>":
                        kwargs[key] = document
                    elif value == "<document_name>":
                        kwargs[key] = document[self.tab.entity.name]
                    elif value == "<document_id>":
                        kwargs[key] = document["_id"]
                    elif value == "<browser>":
                        kwargs[key] = self.tab.browser

                # Execute callback with provided kwargs
                callback = partial(func, **kwargs)
                callback()

        # What happens on click depends on the kwargs
        # Depending on the situation, the function may need a list of documents, or run the function
        # for each document, or manipulate the browser altogether
        args = ["<document>", "<document_id>", "<document_name>"]
        if any([arg in args for arg in menu_action.kwargs.values()]):
            action.triggered.connect(execute_on_each_document)
            return

        action.triggered.connect(execute_on_all_documents)
