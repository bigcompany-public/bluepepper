import argparse
import os
import traceback
from pathlib import Path

import qtawesome
from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtWidgets import QListWidget, QListWidgetItem, QWidget

from bluepepper.core import codex, database
from bluepepper.gui.screenshot_gink import capture_screenshot
from bluepepper.gui.utils import format_widgets, get_stylesheet, get_theme
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.tools.helpme.ui_helpme_widget import Ui_helpme_widget


class ScreenshotItem(QListWidgetItem):
    def __init__(self, path: Path, icon_size: int):
        super().__init__()
        self.path = Path(path)
        pix = QPixmap(str(self.path))
        scaled = pix.scaled(
            QSize(icon_size, icon_size), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        self.setIcon(QIcon(scaled))


class HelpMeWidget(Ui_helpme_widget):
    """This is a template for bluepepper's widgets"""

    def __init__(
        self,
        parent: QWidget,
        path: Path | None = None,
        error: str = "",
        traceback: str = "",
        asset_id: str = "",
        shot_id: str = "",
    ):
        self._parent = parent
        self._error = error
        self._traceback = traceback
        self._path: str = Path(path).as_posix() if path else None  # type: ignore
        self._asset_id = asset_id
        self._shot_id = shot_id
        self._fields: dict[str, str] = self.get_fields() if self._path else None
        self.setup_ui()
        self.setup_signals()
        self.setup_initial_state()
        self.apply_stylesheet()

    def setup_ui(self):
        """Setups the widget exported from QtDesigner inside the parent widget"""
        self.setupUi(self._parent)
        self.list_screenshots.setIconSize(
            QSize(self.screenshot_size, self.screenshot_size)
        )
        self.list_screenshots.setSpacing(5)
        self.list_screenshots.setUniformItemSizes(True)
        self.list_screenshots.setResizeMode(QListWidget.Adjust)

    def setup_signals(self):
        """Creates signals for the various widgets"""
        self.pb_add_screenshot.clicked.connect(self.pb_screenshot_clicked)
        self.list_screenshots.itemSelectionChanged.connect(
            self.screenshot_selection_changed
        )
        self.pb_remove_screenshot.clicked.connect(self.pb_remove_screenshot_clicked)

    def setup_initial_state(self):
        """Sets default values for the various widgets"""
        self.set_current_path()
        self.set_asset()
        self.set_shot()
        self.set_user()
        self.set_computer()
        self.set_error()
        self.set_traceback()
        self.pb_remove_screenshot.setDisabled(True)

    def apply_stylesheet(self):
        """Applies bluepepper's stylesheet. May be used to force a redraw"""
        self._parent.setStyleSheet(get_stylesheet())
        format_widgets(self._parent)

    def get_current_path(self) -> None:
        if self._path:
            return
        self._path = ""

    def get_fields(self) -> dict[str, str] | None:
        try:
            return codex.get_fields(self._path)
        except:  # noqa: E722
            return

    def set_current_path(self) -> None:
        self.get_current_path()
        if not self._path:
            self.l_file.setHidden(True)
            self.label_file.setHidden(True)
        else:
            self.label_file.setText(Path(self._path).as_posix())

    def get_asset_document(self) -> dict[str, str] | None:
        if self._asset_id:
            return database.get_asset_document_by_id(self._asset_id)

        if self._fields:
            if "asset" in self._fields:
                return database.get_asset_document_by_fields(self._fields)

    def set_asset(self) -> None:
        asset_document = self.get_asset_document()
        if not asset_document:
            self.l_asset.setHidden(True)
            self.label_asset.setHidden(True)
            return

        self.label_asset.setText(codex.convs.asset_identifier.format(asset_document))

    def get_shot_document(self) -> dict[str, str] | None:
        if self._shot_id:
            return database.get_shot_document_by_id(self._shot_id)

        if self._fields:
            if "shot" in self._fields:
                return database.get_shot_document_by_fields(self._fields)

    def set_shot(self) -> None:
        shot_document = self.get_shot_document()
        if not shot_document:
            self.l_shot.setHidden(True)
            self.label_shot.setHidden(True)
            return

        self.label_shot.setText(codex.convs.shot_identifier.format(shot_document))

    def get_user(self) -> str:
        return os.environ["USERNAME"]

    def set_user(self) -> None:
        self.label_user.setText(self.get_user())

    def get_computer(self) -> str:
        return os.environ["COMPUTERNAME"]

    def set_computer(self) -> None:
        self.label_computer.setText(self.get_computer())

    def set_error(self) -> None:
        if self._error:
            self.label_error.setText(self._error)
        else:
            self.sa_error.setHidden(True)
            self.l_error.setHidden(True)

    def set_traceback(self) -> None:
        if self._traceback:
            self.label_traceback.setText(self._traceback)
        else:
            self.sa_traceback.setHidden(True)
            self.l_traceback.setHidden(True)

    def pb_screenshot_clicked(self):
        self._parent.showMinimized()
        path = capture_screenshot()
        self._parent.showNormal()
        if not path:
            return
        item = ScreenshotItem(path, self.screenshot_size)
        self.list_screenshots.addItem(item)

    def pb_remove_screenshot_clicked(self):
        selected_items = self.list_screenshots.selectedItems()
        if not selected_items:
            return

        items_num = self.list_screenshots.count()
        for i in range(items_num):
            item = self.list_screenshots.item(i)
            if item in selected_items:
                self.list_screenshots.takeItem(i)

    def screenshot_selection_changed(self):
        enable = bool(self.list_screenshots.selectedItems())
        self.pb_remove_screenshot.setEnabled(enable)

    @property
    def screenshot_size(self) -> int:
        return 200


def show_dialog(
    path: Path | None = None,
    error: str = "",
    traceback: str = "",
    asset_id: str = "",
    shot_id: str = "",
):
    """
    This function pops the main window open.
    May be used directly from your preferred IDE
    """
    app = get_qt_app()

    icon = qtawesome.icon("fa5s.hand-sparkles", scale_factor=1, color=get_theme()["ok"])
    widget = QWidget()
    ui = HelpMeWidget(
        parent=widget,
        path=path,
        error=error,
        traceback=traceback,
        asset_id=asset_id,
        shot_id=shot_id,
    )
    container = ContainerWidget(widget=widget, title="Help Me", icon=icon)
    dialog = ContainerDialog(container=container)
    dialog.exec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=False)
    parser.add_argument("-e", "--error", required=False)
    parser.add_argument("-a", "--asset_id", required=False)
    parser.add_argument("-s", "--shot_id", required=False)
    args = parser.parse_args()

    _error = None
    _traceback = None
    if args.error:
        try:
            raise RuntimeError(args.error)
        except RuntimeError as _err:
            _error = str(_err)
            _traceback = traceback.format_exc()

    show_dialog(
        path=args.path,
        error=_error,
        traceback=_traceback,
        asset_id=args.asset_id,
        shot_id=args.shot_id,
    )
