import subprocess
from argparse import ArgumentParser

import qtawesome
from bson import ObjectId
from pymongo.collection import Collection
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bluepepper.clipboard import clear_clipboard
from bluepepper.core import database
from bluepepper.gui.utils import get_qta_icon, get_theme
from bluepepper.gui.widgets.colorwheel import pick_color
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.tools.tags.tag_widget import TagWidget

_BRIGHTNESS_THRESHOLD = 0.55


def _hex_brightness(hex_color: str) -> float:
    """Return perceived brightness [0, 1] for a CSS hex color string."""
    color = QColor(hex_color)
    r, g, b = color.redF(), color.greenF(), color.blueF()
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _icon_color_for_bg(hex_color: str) -> str:
    """Return '#000000' or '#FFFFFF' depending on background brightness."""
    return (
        "#000000" if _hex_brightness(hex_color) > _BRIGHTNESS_THRESHOLD else "#FFFFFF"
    )


class ColorButton(QPushButton):
    """
    A push-button whose background IS the color swatch.
    - Eyedropper icon flips black/white based on luminance.
    - Ctrl+C while hovered copies the hex to clipboard.
    - Ctrl+V while hovered pastes a valid hex color.
    """

    color_copy_requested = Signal()
    color_paste_requested = Signal(str)

    _EYEDROPPER_ICON = "ph.eyedropper-fill"
    _BUTTON_SIZE = 40

    def __init__(self, initial_color: str, parent=None):
        super().__init__(parent)
        self._color: str = initial_color
        self._hovered: bool = False
        self._theme: dict[str, str] = get_theme()

        self.setMinimumWidth(self._BUTTON_SIZE)
        self.setMinimumHeight(self._BUTTON_SIZE)
        from PySide6.QtCore import Qt

        self.setFocusPolicy(self.focusPolicy() | Qt.StrongFocus)
        self.setMouseTracking(True)
        self._refresh_appearance()

    @property
    def color(self) -> str:
        return self._color

    def set_color(self, hex_color: str):
        self._color = hex_color
        self._refresh_appearance()

    def _refresh_appearance(self):
        icon_color = _icon_color_for_bg(self._color)
        icon = qtawesome.icon(
            self._EYEDROPPER_ICON, scale_factor=1.35, color=icon_color
        )
        self.setIcon(icon)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self._color};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                border: 1px solid {self._theme["active"]};
            }}
            """
        )

    def enterEvent(self, event):
        self._hovered = True
        self.setFocus()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.clearFocus()
        super().leaveEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        from PySide6.QtCore import Qt

        if self._hovered:
            if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
                QApplication.clipboard().setText(self._color)
                self.color_copy_requested.emit()
                return
            if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
                text = QApplication.clipboard().text().strip()
                if QColor(text).isValid():
                    self.color_paste_requested.emit(text)
                    return
        super().keyPressEvent(event)


class TagEditorWidget(QWidget):
    confirmed = Signal()

    def __init__(self, document_id: str, collection: Collection):
        super().__init__()
        self.document: dict = collection.find_one({"_id": ObjectId(document_id)})
        if not self.document:
            raise RuntimeError(
                f"Document not found on database/{collection.name} : {document_id}"
            )
        self.collection = collection

        # Color buffers — hold last confirmed colors for reverting
        self._color_buffer = self.document["tagColor"]
        self._icon_color_buffer = self.document["tagIconColor"]
        self._text_color_buffer = self.document["tagTextColor"]

        # Clipboard watcher timer (for qta-browser icon picking)
        self._icon_timer = QTimer(self)
        self._qta_process: subprocess.Popen | None = None

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

        # Background Color
        self.color_button = ColorButton(self.document["tagColor"])
        form_layout.addRow("Color", self.color_button)

        # Icon Color
        self.icon_color_button = ColorButton(self.document["tagIconColor"])
        form_layout.addRow("Icon Color", self.icon_color_button)

        # Text Color
        self.text_color_button = ColorButton(self.document["tagTextColor"])
        form_layout.addRow("Text Color", self.text_color_button)

        # Icon
        self.pick_icon_button = QPushButton("Pick Icon")
        self.remove_icon_button = QPushButton("Remove Icon")
        self.remove_icon_button.setEnabled(bool(self.document.get("tagIcon")))

        icon_buttons_layout = QHBoxLayout()
        icon_buttons_layout.setContentsMargins(0, 0, 0, 0)
        icon_buttons_layout.addWidget(self.pick_icon_button)
        icon_buttons_layout.addWidget(self.remove_icon_button)
        icon_buttons_layout.addStretch()

        self.icon_row_label = QLabel("Icon")
        form_layout.addRow(self.icon_row_label, icon_buttons_layout)

        # Spacer row
        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(12)
        form_layout.addRow(QLabel(), spacer_widget)

        # Preview
        self.tag_widget = TagWidget(self.document)
        form_layout.addRow("Preview", self.tag_widget)

        # OK button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.ok_button = QPushButton("OK")
        self.ok_button.setProperty("status", "important")
        button_layout.addWidget(self.ok_button)
        main_layout.addLayout(button_layout)

    def _refresh_icon_row(self):
        icon = self.tag_widget._tag_icon or ""
        self.remove_icon_button.setEnabled(bool(icon))

    def setup_signals(self):
        self.color_button.clicked.connect(self.color_button_clicked)
        self.icon_color_button.clicked.connect(self.icon_color_button_clicked)
        self.text_color_button.clicked.connect(self.text_color_button_clicked)

        self.color_button.color_paste_requested.connect(self._on_color_pasted)
        self.icon_color_button.color_paste_requested.connect(self._on_icon_color_pasted)
        self.text_color_button.color_paste_requested.connect(self._on_text_color_pasted)

        self.pick_icon_button.clicked.connect(self.open_icon_browser)
        self.remove_icon_button.clicked.connect(self._remove_icon)
        self._icon_timer.timeout.connect(self._check_clipboard_for_icon)

        self.ok_button.clicked.connect(self.ok_button_clicked)

    def color_button_clicked(self):
        self._color_buffer = self.tag_widget._tag_color
        color = pick_color(
            start_color=self._color_buffer,
            on_color_changed=self._on_color_changed,
        )
        if color:
            self._on_color_accepted(color)
        else:
            self._on_color_rejected()

    def _on_color_changed(self, color: str):
        self.color_button.set_color(color)
        self.tag_widget._tag_color = color
        self.tag_widget.update_preview()

    def _on_color_accepted(self, color: str):
        self._color_buffer = color

    def _on_color_rejected(self):
        self.color_button.set_color(self._color_buffer)
        self.tag_widget._tag_color = self._color_buffer
        self.tag_widget.update_preview()

    def _on_color_pasted(self, color: str):
        self._color_buffer = color
        self.color_button.set_color(color)
        self.tag_widget._tag_color = color
        self.tag_widget.update_preview()

    def icon_color_button_clicked(self):
        self._icon_color_buffer = self.tag_widget._tag_icon_color
        color = pick_color(
            start_color=self._icon_color_buffer,
            on_color_changed=self._on_icon_color_changed,
        )
        if color:
            self._on_icon_color_accepted(color)
        else:
            self._on_icon_color_rejected()

    def _on_icon_color_changed(self, color: str):
        self.icon_color_button.set_color(color)
        self.tag_widget._tag_icon_color = color
        self.tag_widget.update_preview()

    def _on_icon_color_accepted(self, color: str):
        self._icon_color_buffer = color

    def _on_icon_color_rejected(self):
        self.icon_color_button.set_color(self._icon_color_buffer)
        self.tag_widget._tag_icon_color = self._icon_color_buffer
        self.tag_widget.update_preview()

    def _on_icon_color_pasted(self, color: str):
        self._icon_color_buffer = color
        self.icon_color_button.set_color(color)
        self.tag_widget._tag_icon_color = color
        self.tag_widget.update_preview()

    def text_color_button_clicked(self):
        self._text_color_buffer = self.tag_widget._tag_text_color
        color = pick_color(
            start_color=self._text_color_buffer,
            on_color_changed=self._on_text_color_changed,
        )
        if color:
            self._on_text_color_accepted(color)
        else:
            self._on_text_color_rejected()

    def _on_text_color_changed(self, color: str):
        self.text_color_button.set_color(color)
        self.tag_widget._tag_text_color = color
        self.tag_widget.update_preview()

    def _on_text_color_accepted(self, color: str):
        self._text_color_buffer = color

    def _on_text_color_rejected(self):
        self.text_color_button.set_color(self._text_color_buffer)
        self.tag_widget._tag_text_color = self._text_color_buffer
        self.tag_widget.update_preview()

    def _on_text_color_pasted(self, color: str):
        self._text_color_buffer = color
        self.text_color_button.set_color(color)
        self.tag_widget._tag_text_color = color
        self.tag_widget.update_preview()

    def open_icon_browser(self):
        clear_clipboard()
        self._qta_process = subprocess.Popen(["qta-browser"])
        self._icon_timer.start(100)

    def _check_clipboard_for_icon(self):
        process_done = (
            self._qta_process is not None and self._qta_process.poll() is not None
        )
        clipboard_text = QApplication.clipboard().text().strip()

        if clipboard_text:
            if self._qta_process and self._qta_process.poll() is None:
                self._qta_process.terminate()
            self._qta_process = None
            self._icon_timer.stop()
            self._apply_icon(clipboard_text)
        elif process_done:
            self._qta_process = None
            self._icon_timer.stop()

    def _apply_icon(self, icon_name: str):
        self.tag_widget._tag_icon = icon_name
        self.tag_widget.update_preview()
        self._refresh_icon_row()

    def _remove_icon(self):
        self.tag_widget._tag_icon = ""
        self.tag_widget.update_preview()
        self._refresh_icon_row()

    def ok_button_clicked(self):
        self.collection.update_one(
            {"_id": self.document["_id"]},
            {
                "$set": {
                    "tagColor": self.tag_widget._tag_color,
                    "tagIconColor": self.tag_widget._tag_icon_color,
                    "tagTextColor": self.tag_widget._tag_text_color,
                    "tagIcon": self.tag_widget._tag_icon,
                }
            },
        )
        self.document: dict = self.collection.find_one(
            {"_id": ObjectId(self.document["_id"])}
        )  # type: ignore
        self.confirmed.emit()


def edit_asset_tag(document_id) -> dict[str, str] | None:
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    widget = TagEditorWidget(document_id, database.asset_tags)
    container = ContainerWidget(widget=widget, icon=icon, title="Edit Tag")
    dialog = ContainerDialog(container)
    widget.confirmed.connect(dialog.accept)
    if dialog.exec():
        return widget.document


def edit_shot_tag(document_id):
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    widget = TagEditorWidget(document_id, database.shot_tags)
    container = ContainerWidget(widget=widget, icon=icon, title="Edit Tag")
    dialog = ContainerDialog(container)
    widget.confirmed.connect(dialog.accept)
    if dialog.exec():
        return widget.document


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-aid", "--asset_id", required=False)
    parser.add_argument("-sid", "--shot_id", required=False)
    args = parser.parse_args()

    if args.asset_id:
        print(edit_asset_tag(args.asset_id))

    if args.shot_id:
        print(edit_shot_tag(args.shot_id))
