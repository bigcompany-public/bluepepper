from __future__ import annotations

import logging
from argparse import ArgumentParser

from qtpy.QtCore import QEvent, Signal
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from bluepepper.core import database, init_logging
from bluepepper.database import Collection, ObjectId
from bluepepper.gui.utils import get_qta_icon, get_theme
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.tools.tags.tag_creator_widget import show_dialog
from bluepepper.tools.tags.tag_editor_widget import edit_tag
from bluepepper.tools.tags.tag_widget import TagWidget


class TagDeletionWarningWidget(QWidget):
    confirmed = Signal()
    rejected = Signal()

    def __init__(self, tag: str, num: int, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(
            f'The tag "{tag}" is used in {num} entities. Are you sure you want to remove this tag, and unlink it ?'
        )
        layout.addWidget(label)
        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)
        layout.addWidget(bottom_frame)
        bottom_layout.addStretch()

        # Buttons
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        bottom_layout.addWidget(self.cancel_button)
        self.yes_button = QPushButton("Yes")

        self.yes_button.setProperty("status", "danger")
        self.yes_button.clicked.connect(self.yes_button_clicked)
        bottom_layout.addWidget(self.yes_button)

    def yes_button_clicked(self):
        self.confirmed.emit()

    def cancel_button_clicked(self):
        self.rejected.emit()


def show_tag_deletion_warning_dialog(tag: str, num: int, parent=None) -> int:
    app = get_qt_app()
    icon = get_qta_icon(name="ph.warning-fill", scale_factor=1.25, color=get_theme()["warning"])
    widget = TagDeletionWarningWidget(parent=None, tag=tag, num=num)
    container = ContainerWidget(widget=widget, icon=icon, title="Tag Manager")
    dialog = ContainerDialog(container)
    widget.confirmed.connect(dialog.accept)
    widget.rejected.connect(dialog.reject)
    return dialog.exec()


class EditableTagWidget(QWidget):
    """
    Warning: adding a widget to a QTableWidgetItem somehow messes up its size policy, which expands to fill the
    cell. To fix this, this widget acts as a container for the actual TagWidget, with a stretch added to properly
    align the TagWidget to the left
    """

    def __init__(
        self,
        tag_document: dict[str, str],
        tag_manager: TagManagerWidget,
    ):
        super().__init__(tag_manager)
        self.tag_document = tag_document
        self.tag_document_widget = tag_manager

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._widget = TagWidget(tag_document=tag_document)
        self._layout.addWidget(self._widget)
        self._layout.addStretch()

    def update_tag_widget(self):
        self._widget.deleteLater()
        self._widget = TagWidget(tag_document=self.tag_document)
        self._layout.insertWidget(0, self._widget)

    def edit_tag(self):
        result = edit_tag(str(self.tag_document["_id"]))
        if result:
            self.tag_document = result
            self.update_tag_widget()


class TagTableWidget(QTableWidget):
    def __init__(self, tag_manager: TagManagerWidget):
        super().__init__(tag_manager)
        self.tag_manager = tag_manager
        self.setColumnCount(1)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)

    def update_items(self) -> None:
        # Store selection
        selection = [document["_id"] for document in self.selected_documents]

        # Get documents & create items
        self.clear()
        documents = self.tag_manager.get_tag_documents()
        self.setRowCount(len(documents))
        for row, document in enumerate(documents):
            widget = EditableTagWidget(document, self.tag_manager)
            item = QTableWidgetItem()
            self.setItem(row, 0, item)
            self.setCellWidget(row, 0, widget)
            self.setRowHeight(row, widget.sizeHint().height() + 4)

            # Restore selection
            if document["_id"] in selection:
                item.setSelected(True)

    def get_tag_widget_at_row(self, row: int) -> EditableTagWidget:
        return self.cellWidget(row, 0)  # type: ignore

    @property
    def selected_tag_widgets(self) -> list[EditableTagWidget]:
        return [self.get_tag_widget_at_row(item.row()) for item in self.selectedItems()]

    @property
    def selected_documents(self) -> list[dict[str, str]]:
        return [widget.tag_document for widget in self.selected_tag_widgets]

    def contextMenuEvent(self, event: QEvent):
        """
        This method pops a Qmenu widget when the user right clicks on the table
        """
        if not self.selectedItems():
            return

        menu = TagManagerMenu(table_widget=self)
        menu.exec_(event.globalPos())


class TagManagerMenu(QMenu):
    def __init__(self, table_widget: TagTableWidget):
        super().__init__(table_widget)
        self.table_widget = table_widget

        # Actions
        edit_action = self.addAction("Edit")
        edit_action.triggered.connect(self.edit_tags)
        delete_action = self.addAction("Delete")
        delete_action.triggered.connect(self.delete_tags)

    def edit_tags(self):
        for document in self.table_widget.selected_documents:
            edit_tag(document_id=document["_id"])
        self.table_widget.update_items()

    def delete_tags(self):
        for document in self.table_widget.selected_documents:
            self.delete_tag(document)
        self.table_widget.update_items()

    def delete_tag(self, document: dict):
        tag = document["tag"]
        collection: Collection = getattr(database.db, document["tagCollection"])
        entities_with_tag = database.get_entities_with_tag(tag, collection)
        if entities_with_tag:
            if not show_tag_deletion_warning_dialog(tag=tag, num=len(entities_with_tag)):
                return

        for entity in entities_with_tag:
            print(entity)
            all_tags: list = entity.get("_tags", [])
            logging.warning(f'Removing tag "{tag}" from entity : {entity}')
            all_tags.remove(tag)
            collection.update_one({"_id": ObjectId(entity["_id"])}, {"$set": {"_tags": all_tags}})

        logging.warning(f"Removing document : {document['tag']}")
        database.tags.delete_one({"_id": ObjectId(document["_id"])})


class TagManagerWidget(QWidget):
    confirmed: Signal = Signal(object)

    def __init__(self, tag_collection: str):
        self.tag_collection = tag_collection
        super().__init__()
        self.setup_ui()
        self.setup_signals()
        self.setup_initial_state()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Search bar
        top_frame = QFrame()
        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(top_frame)
        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("Search tags...")
        top_frame_layout.addWidget(self._search_edit)

        # Create button
        self.create_button = QPushButton("New")
        self.create_button.setFixedWidth(50)
        self.create_button.setProperty("status", "important")
        top_frame_layout.addWidget(self.create_button)

        # Table
        frame = QFrame()
        frame.setProperty("depth", "0")
        layout.addWidget(frame)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        frame_layout.setContentsMargins(3, 3, 3, 3)
        self.table_widget = TagTableWidget(self)
        frame_layout.addWidget(self.table_widget)
        button_row = QHBoxLayout()
        button_row.addStretch()

        # Ok button
        self._ok_button = QPushButton("OK")
        self._ok_button.setFixedWidth(50)
        self._ok_button.setProperty("status", "important")
        button_row.addWidget(self._ok_button)
        layout.addLayout(button_row)

        self.setMinimumWidth(250)

    def setup_signals(self) -> None:
        self._search_edit.textChanged.connect(self.table_widget.update_items)
        self._ok_button.clicked.connect(lambda: self.confirmed.emit(self.selected_documents))
        self.create_button.clicked.connect(self.create_button_clicked)

    def create_button_clicked(self):
        document = show_dialog(self.tag_collection, tag_name=self._search_edit.text())
        if not document:
            return

        # Select newly created item
        self.table_widget.update_items()
        self.table_widget.clearSelection()
        for row in range(self.table_widget.rowCount()):
            widget = self.table_widget.get_tag_widget_at_row(row)
            item: QTableWidgetItem = self.table_widget.item(row, 0)  # type: ignore
            if widget.tag_document["_id"] == document["_id"]:
                item.setSelected(True)

    @property
    def selected_documents(self) -> list[dict[str, str]]:
        return self.table_widget.selected_documents

    def get_tag_documents(self) -> list[dict[str, str]]:
        query = {"tag": {"$regex": self._search_edit.text(), "$options": "i"}, "tagCollection": self.tag_collection}
        return sorted(list(database.tags.find(query)), key=lambda doc: doc["tag"])

    def setup_initial_state(self) -> None:
        self.table_widget.update_items()


def show_tag_manager_dialog(tag_collection: str) -> list[dict[str, str]] | None:
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    widget = TagManagerWidget(tag_collection)
    container = ContainerWidget(widget=widget, icon=icon, title="Tag Manager")
    dialog = ContainerDialog(container)
    widget.confirmed.connect(dialog.accept)
    if dialog.exec():
        return widget.selected_documents


if __name__ == "__main__":
    init_logging("sandbox")
    parser = ArgumentParser()
    parser.add_argument("-t", "--tag_collection", required=True)
    args = parser.parse_args()
    print(show_tag_manager_dialog(args.tag_collection))
