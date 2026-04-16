from __future__ import annotations

import importlib
import json
import logging
from functools import partial
from json.decoder import JSONDecodeError
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

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_config import Entity, MenuAction
    from bluepepper.tools.browser.browser_tab import (
        EntityTab,
        FilterComboBox,
        SearchBar,
    )
    from bluepepper.tools.browser.browser_widget import BrowserWidget


class TableDocuments(QTableWidget):
    """
    This class adds signals to the provided table widget
    This method was chosen over inheriting from QTableWidget and initializing a
    new widget to keep as much control as possible in QtDesigner
    """

    def __init__(self, tab: EntityTab):
        self.tab = tab
        self.browser: BrowserWidget = tab.browser
        self.entity: Entity = tab.entity
        self.search_bar: SearchBar = tab.search_bar
        self.filter_comboboxes: list[FilterComboBox] = tab.filter_comboboxes
        self.collection = database.db.get_collection(self.entity.collection)
        self.document_items: list[DocumentItem] = []
        self.buffered_document_selection: list[dict] = []
        super().__init__(tab)
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        self.setColumnCount(1)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        item = QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        self.setHorizontalHeaderLabels(["Documents"])
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
        self.itemSelectionChanged.connect(self.document_selection_changed)

    def document_selection_changed(self):
        """This method is triggered when the document's selection has changed"""
        document_names = [doc.text() for doc in self.selectedItems()]
        logging.info(f"Document selection changed to {document_names}")
        self.tab.task_table.update_items()
        self.tab.file_table.update_items()

    def get_mongodb_query(self) -> dict:
        """Generates a mongodb query from the search bar and filters"""
        search = self.tab.search_bar.text().strip()
        # cover hard-written queries
        if search.startswith("{"):
            try:
                return json.loads(search)
            except JSONDecodeError:
                return {"error": "Invalid query"}

        query: dict[str, str] = {}

        # Get exact value for non-name fields
        query = {
            filter_combobox.filter: filter_combobox.currentText().strip()
            for filter_combobox in self.filter_comboboxes
            if not filter_combobox.currentText() == "*"
        }

        # Construct name query
        search = self.tab.search_bar.text()
        name_search_list = [
            string.strip() for string in search.split(";") if string.strip()
        ]
        if name_search_list:
            # Compose name query
            name_query = []
            for string in name_search_list:
                name_query.append(
                    {self.entity.name: {"$regex": string, "$options": "i"}}
                )
            query["$or"] = name_query

        return query

    def get_documents(self, query: dict) -> list[dict]:
        if query.get("error"):
            return []

        _documents = list(self.collection.find(query))
        documents = []
        for doc in _documents:
            # _id is an ObjectId instance, not string
            # This may cause issues when serializing documents
            doc["_id"] = str(doc["_id"])
            documents.append(doc)
        documents.sort(key=lambda doc: doc[self.entity.name])
        return documents

    def update_items(self):
        """
        This method updates the table documents with mongoDB documents
        that match the query
        """
        # Block signals, to prevent other parts of the ui to be updated, while items are removed
        # or re-selected
        self.blockSignals(True)

        # Buffer the current selection, in order to re-select documents if needed and to know if
        # updating the tasks is required
        self.buffered_document_selection = self.selected_documents
        buffered_ids = [doc["_id"] for doc in self.buffered_document_selection]

        # Remove all items
        self.clear_items()

        # Get new documents that match the query formulated by search bar and fields
        query = self.get_mongodb_query()
        documents = self.get_documents(query)

        # Create dummy item if nothing matches the query
        if not documents:
            self.document_items = [DocumentItem()]

        # Create a new item for each document
        for document in documents:
            new_item = DocumentItem(document, self.entity)
            self.document_items.append(new_item)

        # Add items to the table
        new_selected_documents: list[str] = []
        for item in self.document_items:
            row_number = self.rowCount()
            self.insertRow(row_number)
            self.setItem(row_number, 0, item)

            # Reselect the item if it was already selected
            if item.document:
                if item.document["_id"] in buffered_ids:
                    item.setSelected(True)
                    new_selected_documents.append(item.document)

        # Re-enable signals
        self.blockSignals(False)

        # Force update if the selection actually changed
        new_ids = [doc["_id"] for doc in new_selected_documents]
        if new_ids != buffered_ids:
            self.document_selection_changed()

    def clear_items(self):
        self.clearContents()
        self.setRowCount(0)
        self.document_items = []

    @property
    def selected_documents(self) -> list[dict[str, str]]:
        """Returns the list of selected documents as a list of dict"""
        items = self.selectedItems() or []
        items = [item for item in items if isinstance(item, DocumentItem)]
        documents = [item.document for item in items]
        return documents

    def contextMenuEvent(self, event: QEvent):
        """
        This method pops a Qmenu widget when the user right clicks on the table
        """
        if not self.entity.document_actions:
            return
        menu = TableDocumentsMenu(tab=self.tab, event=event)
        menu.exec_(event.globalPos())


class DocumentItem(QTableWidgetItem):
    """This class represents a document item within the TableDocuments widget"""

    def __init__(self, document: dict[str, str] = None, entity: Entity = None):
        self.document = document
        self.entity = entity
        self.label: str = ""
        super().__init__("")
        self.set_label()
        self.set_enabled()
        self.set_tooltip()

    def set_tooltip(self):
        if self.document:
            self.setToolTip(json.dumps(self.document, indent=4))

    def set_label(self):
        label = (
            self.document[self.entity.name] if self.document else "No documents found"
        )
        self.setText(label)

    def set_enabled(self):
        if not self.document:
            self.setFlags(self.flags() ^ Qt.ItemFlag.ItemIsEnabled)


class TableDocumentsMenu(QMenu):
    def __init__(self, tab: EntityTab, event: QEvent):
        super().__init__(tab)
        self.tab = tab
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
        for action in self.entity.document_actions:
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

                # Execute callback with provided kwargs
                callback = partial(func, **kwargs)
                callback()

        # The following arguments are indicators the callback must be called on each document
        args = ["<document>", "<document_id>", "<document_name>"]
        if any([arg in args for arg in menu_action.kwargs.values()]):
            action.triggered.connect(execute_on_each_document)
        else:
            action.triggered.connect(execute_on_all_documents)
