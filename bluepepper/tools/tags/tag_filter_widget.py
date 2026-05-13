from __future__ import annotations

from argparse import ArgumentParser

from qtpy.QtCore import Qt, Signal
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
    def __init__(self, tag_document: dict[str, str], item: QListWidgetItem):
        super().__init__()
        self.tag_document = tag_document
        self.item = item

        margin_layout = QVBoxLayout(self)
        margin_layout.setContentsMargins(0, 0, 0, 0)

        inner_frame = QFrame()
        inner_frame.setProperty("depth", "1")
        inner_frame.setContentsMargins(0, 0, 0, 0)
        inner_frame.setStyleSheet("")
        margin_layout.addWidget(inner_frame)
        self._layout = QHBoxLayout(inner_frame)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._widget = TagWidget(tag_document=tag_document)
        self._layout.addWidget(self._widget)
        self._layout.addStretch()
        self.update_color()

    def update_item_size_hint(self):
        """Call this after setItemWidget() so layout is finalized."""
        self.adjustSize()
        size = self.sizeHint()
        size.setHeight(size.height() + 2)
        self.item.setSizeHint(size)

    def update_color(self, grey_out=True):
        self._widget.update_preview(greyed_out=grey_out)


class TagList(QListWidget):
    def __init__(self, tag_filter_widget: TagFilterWidget):
        super().__init__(tag_filter_widget)
        self.tag_filter_widget = tag_filter_widget

        # UI
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setWrapping(True)
        self.setSpacing(1)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)

        # Signals
        self.itemSelectionChanged.connect(self.selection_changed)

    def selection_changed(self):
        for i in range(self.count()):
            item = self.item(i)
            widget: TagListWidget = self.itemWidget(item)  # type: ignore
            widget.update_color(grey_out=not item.isSelected())

    @property
    def all_widgets(self) -> list[TagListWidget]:
        widgets = []
        for i in range(self.count()):
            item = self.item(i)
            widget: TagListWidget = self.itemWidget(item)  # type: ignore
            widgets.append(widget)
        return widgets

    @property
    def selected_tags(self) -> list[str]:
        tags = []
        for i in range(self.count()):
            item = self.item(i)
            if not item.isSelected():
                continue
            widget: TagListWidget = self.itemWidget(item)  # type: ignore
            tags.append(widget.tag_document["tag"])
        return tags


class TagFilterWidget(QWidget):
    confirmed: Signal = Signal(object)

    def __init__(self, tag_collection: str):
        self.tag_collection = tag_collection
        super().__init__()
        self.setup_ui()
        self.setup_initial_state()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.list_widget = TagList(self)
        layout.addWidget(self.list_widget)

    def get_tag_documents(self) -> list[dict]:
        documents = list(database.tags.find({"tagCollection": self.tag_collection}))
        return sorted(documents, key=lambda doc: doc["tag"])

    def setup_initial_state(self):
        self.update_items()

    def update_items(self):
        self.list_widget.clear()
        for document in self.get_tag_documents():
            item = QListWidgetItem()
            widget = TagListWidget(tag_document=document, item=item)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

            # Now the widget is parented and layout is computable
            widget.update_item_size_hint()

    @property
    def selected_tags(self) -> list[str]:
        return self.list_widget.selected_tags

    @property
    def all_widgets(self) -> list[TagListWidget]:
        return self.list_widget.all_widgets


def show_dialog(tag_collection: str) -> list[str] | None:
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
