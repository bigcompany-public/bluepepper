import qtawesome
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)


class TagWidget(QFrame):
    def __init__(self, tag_document: dict[str, str], size: int = 26):
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
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self._size)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        self.icon_label = QLabel()
        self.text_label = QLabel(self._tag)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setMargin(2)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

    def update_preview(self, greyed_out: bool = False):
        # Adjust colors if greyed out
        tag_color = self._tag_color
        tag_text_color = self._tag_text_color
        tag_icon_color = self._tag_icon_color
        if greyed_out:
            tag_color = "#8A8A8A"
            tag_text_color = "#111111"
            tag_icon_color = "#111111"

        # Set text value
        self.text_label.setText(self._tag)

        # Set icon
        if self._tag_icon:
            try:
                icon = qtawesome.icon(self._tag_icon, color=tag_icon_color)
                self.icon_label.setPixmap(icon.pixmap(int(self._size * 0.75), int(self._size * 0.75)))
                self.icon_label.setHidden(False)
            except Exception:
                self.icon_label.setHidden(True)
        else:
            self.icon_label.setHidden(True)

        # Set stylesheet
        right_padding = self._size / 2
        left_padding = right_padding if self.icon_label.isHidden() else right_padding / 2
        self.setStyleSheet(
            f"""
            background-color: {tag_color};
            color: {tag_text_color};
            font-weight: bold;
            font-size:{int(self._size * 0.5)}px;
            border-radius: {int(self._size / 2)}px;
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
