from argparse import ArgumentParser

import qtawesome
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)

from bluepepper.core import database
from bluepepper.gui.utils import get_qta_icon
from bluepepper.gui.widgets.container import ContainerWidget, get_qt_app


class TagWidget(QFrame):
    def __init__(self, tag_document: dict[str, str], size: int = 24):
        super().__init__()
        self.document = tag_document
        self._size = size
        self._tag = self.document["tag"]
        self._tag_color = self.document["tagColor"]
        self._tag_icon = self.document["tagIcon"]
        self._tag_icon_color = self.document["tagIconColor"]
        self._tag_text_color = self.document["tagTextColor"]
        self.setup_ui()
        self.update_preview()

    def setup_ui(self):
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedHeight(self._size)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        self.icon_label = QLabel()
        self.text_label = QLabel(self._tag)
        self.text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

    def update_preview(self):

        self.text_label.setText(self._tag)

        if self._tag_icon:
            try:
                icon = qtawesome.icon(self._tag_icon, color=self._tag_icon_color)
                self.icon_label.setPixmap(
                    icon.pixmap(int(self._size * 0.75), int(self._size * 0.75))
                )
                self.icon_label.setHidden(False)
            except Exception:
                self.icon_label.setHidden(True)
        else:
            self.icon_label.setHidden(True)

        right_padding = self._size / 2
        left_padding = (
            right_padding if self.icon_label.isHidden() else right_padding / 2
        )

        self.setStyleSheet(
            f"""
            background-color: {self._tag_color};
            color: {self._tag_text_color};
            font-weight: bold;
            border-radius: {self._size / 2}px;
            padding-left:{left_padding}px;
            padding-right:{right_padding}px;
            """
        )
        self.text_label.setStyleSheet(
            """
            background-color: none;
            padding-left:0px;
            padding-right:0px;
            """
        )
        self.icon_label.setStyleSheet(
            """
            padding-left:0px;
            padding-right:0px;
            background-color: none;
            """
        )


def show_asset_tag(document_id):
    document = database.get_asset_tag_document_by_id(document_id)
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    from qtpy.QtWidgets import QLabel, QTableWidget, QTableWidgetItem

    table = QTableWidget()
    table.setColumnCount(1)
    table.insertRow(0)
    item = QTableWidgetItem("Jaj")
    # item.setText("JAJ")
    l = QLabel()
    table.setItem(0, 0, item)
    widget = TagWidget(document)
    table.setCellWidget(0, 0, widget)
    # table.setItem(0, 0, item)
    container = ContainerWidget(widget=table, icon=icon, title="Tag")
    container.show()
    app.exec()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-aid", "--asset_id", required=False)
    parser.add_argument("-sid", "--shot_id", required=False)
    args = parser.parse_args()

    if args.asset_id:
        print(show_asset_tag(args.asset_id))
