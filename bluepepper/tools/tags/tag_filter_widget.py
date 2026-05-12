from __future__ import annotations

from argparse import ArgumentParser

from qtpy.QtCore import QSize, Qt, Signal
from qtpy.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QListView,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
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
from bluepepper.tools.tags.tag_widget import TagWidget


class TagListWidget(QFrame):
    """
    Frame that contains the actual TagWidget, mostly for having a good looking and well spaced table items
    """

    def __init__(self, tag_document: dict[str, str], item: QListWidgetItem):
        super().__init__()
        self.tag_document = tag_document
        self.item = item

        # Add a container with a few pixels of margin to make the selection more visually clear in the JobTableWidget
        margin_layout = QVBoxLayout(self)
        margin_layout.setContentsMargins(2, 0, 0, 0)

        # Main frame containing the tag widget
        inner_frame = QFrame()
        inner_frame.setProperty("depth", "4")
        margin_layout.addWidget(inner_frame)
        self._layout = QHBoxLayout(inner_frame)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layout.setContentsMargins(2, 2, 2, 2)
        self._widget = TagWidget(tag_document=tag_document)
        self._layout.addWidget(self._widget)
        self._layout.addStretch()

        # Adjust the size of the item
        size: QSize = self.sizeHint()
        item.setSizeHint(size)


class TagList(QListWidget):
    def __init__(self, tag_filter_widget: TagFilterWidget):
        super().__init__(tag_filter_widget)
        self.tag_filter_widget = tag_filter_widget
        self.setResizeMode(QListView.ResizeMode.Adjust)
        # self.setGridSize(QSize(64, 64))
        self.setSortingEnabled(True)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setWrapping(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setFixedHeight(50)


class TagFilterWidget(QWidget):
    confirmed: Signal = Signal(object)

    def __init__(self, tag_collection: str):
        self.tag_collection = tag_collection
        super().__init__()
        self.setup_ui()
        self.setup_signals()
        self.setup_initial_state()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.list_widget = TagList(self)
        layout.addWidget(self.list_widget)

    def get_tag_documents(self) -> list[dict]:
        documents = list(database.tags.find({"tagCollection": self.tag_collection}))
        return sorted(documents, key=lambda doc: doc["tag"])

    def setup_signals(self):
        pass

    def setup_initial_state(self):
        for document in self.get_tag_documents():
            # Item
            item = QListWidgetItem()
            item.setText(document["tag"])

            # Widget
            widget = TagListWidget(tag_document=document, item=item)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

    @property
    def selected_tags(self) -> list[dict]:
        return []


def show_dialog(tag_collection: str) -> list[dict[str, str]] | None:
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    widget = TagFilterWidget(tag_collection)
    container = ContainerWidget(widget=widget, icon=icon, title="Tag Grid")
    dialog = ContainerDialog(container)
    widget.confirmed.connect(dialog.accept)
    if dialog.exec():
        return widget.selected_tags


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--tag_collection", required=True)
    args = parser.parse_args()

    show_dialog(tag_collection=args.tag_collection)
