from argparse import ArgumentParser
from typing import Callable

from pymongo.collection import Collection
from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QMenu,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from bluepepper.core import database
from bluepepper.gui.utils import get_qta_icon
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.tools.tags.tag_editor_widget import edit_asset_tag, edit_shot_tag
from bluepepper.tools.tags.tag_widget import TagWidget


class EditableTagWidget(QWidget):
    """
    Warning: adding a widget to a QTableWidgetItem somehow messes up its size policy, which expands to fill the
    cell. To fix this, this widget acts as a container for the actual TagWidget, with a stretch added to properly
    align the TagWidget to the left
    """

    def __init__(
        self,
        tag_document: dict[str, str],
        edit_callback: Callable,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._tag_document = tag_document
        self._edit_callback = edit_callback

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._widget = TagWidget(tag_document=tag_document)
        self._layout.addWidget(self._widget)
        self._layout.addStretch()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def update_tag_widget(self):
        self._widget.deleteLater()
        self._widget = TagWidget(tag_document=self._tag_document)
        self._layout.insertWidget(0, self._widget)

    def _show_context_menu(self, pos) -> None:
        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        if menu.exec(self.mapToGlobal(pos)):
            result = self._edit_callback(str(self._tag_document["_id"]))
            if result:
                self._tag_document = result
                self.update_tag_widget()


class TagManagerWidget(QWidget):
    confirmed: Signal = Signal(object)

    def __init__(self, collection: Collection, edit_callback: Callable):
        super().__init__()
        self._collection = collection
        self._edit_callback = edit_callback
        self.setup_ui()
        self.setup_signals()
        self.setup_initial_state()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("Search tags...")
        layout.addWidget(self._search_edit)

        frame = QFrame()
        frame.setProperty("depth", "0")
        layout.addWidget(frame)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        frame_layout.setContentsMargins(3, 3, 3, 3)
        self._table = QTableWidget()
        self._table.setColumnCount(1)
        self._table.horizontalHeader().hide()
        self._table.verticalHeader().hide()
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        frame_layout.addWidget(self._table)

        button_row = QHBoxLayout()
        button_row.addStretch()
        self._ok_button = QPushButton("OK")
        self._ok_button.setProperty("status", "important")
        button_row.addWidget(self._ok_button)
        layout.addLayout(button_row)

        self.setMinimumWidth(250)

    def setup_signals(self) -> None:
        self._search_edit.textChanged.connect(self.update_items)
        self._ok_button.clicked.connect(
            lambda: self.confirmed.emit(self._get_selected_document())
        )

    def _get_selected_document(self) -> dict[str, str] | None:
        selected = self._table.selectedItems()
        if not selected:
            return None
        row = selected[0].row()
        widget = self._table.cellWidget(row, 0)
        return widget._tag_document if isinstance(widget, EditableTagWidget) else None

    def get_tag_documents(self) -> list[dict[str, str]]:
        query = {"tag": {"$regex": self._search_edit.text(), "$options": "i"}}
        return sorted(list(self._collection.find(query)), key=lambda doc: doc["tag"])

    def setup_initial_state(self) -> None:
        self.update_items()

    def update_items(self) -> None:
        documents = self.get_tag_documents()
        self._table.setRowCount(len(documents))
        for row, document in enumerate(documents):
            widget = EditableTagWidget(
                tag_document=document, edit_callback=self._edit_callback
            )
            self._table.setItem(row, 0, QTableWidgetItem())
            self._table.setCellWidget(row, 0, widget)
            self._table.setRowHeight(row, widget.sizeHint().height() + 6)

    def selected_documents(self) -> list[dict[str, str]]:
        documents = []
        item: QTableWidgetItem
        for item in self._table.selectedItems():
            widget: EditableTagWidget = self._table.cellWidget(item.row(), 0)
            documents.append(widget._tag_document)
        return documents


def show_asset_tag_manager_dialog() -> list[dict[str, str]] | None:
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    widget = TagManagerWidget(
        collection=database.asset_tags, edit_callback=edit_asset_tag
    )
    container = ContainerWidget(widget=widget, icon=icon, title="Tag Manager")
    dialog = ContainerDialog(container)
    widget.confirmed.connect(dialog.accept)
    if dialog.exec():
        return widget.selected_documents()


def show_shot_tag_manager_dialog() -> list[dict[str, str]] | None:
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    widget = TagManagerWidget(
        collection=database.shot_tags, edit_callback=edit_shot_tag
    )
    container = ContainerWidget(widget=widget, icon=icon, title="Tag Manager")
    dialog = ContainerDialog(container)
    widget.confirmed.connect(dialog.accept)
    if dialog.exec():
        return widget.selected_documents()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-a", "--asset", action="store_true")
    parser.add_argument("-s", "--shot", action="store_true")
    args = parser.parse_args()

    if args.asset:
        print(show_asset_tag_manager_dialog())

    if args.shot:
        print(show_shot_tag_manager_dialog())
