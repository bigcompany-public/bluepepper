import os
import shutil
import urllib.request
import zipfile
from pathlib import Path

import qtawesome
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from bluepepper.database import database
from bluepepper.gui.widgets.container import ContainerDialog, ContainerWidget, get_qt_app
from conf.naming_conventions import codex


class DemoProjectWidget(QWidget):
    confirmed = Signal()
    rejected = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        title = QLabel("Almost there!")
        title.setProperty("tag", "H2")
        layout.addWidget(title)
        layout.addWidget(
            QLabel(
                "It looks like you're starting a new BluePepper instance.\nWould you like to download a demo project to explore its features?"
            )
        )
        bottom_frame = QFrame()
        layout.addWidget(bottom_frame)
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(0, 20, 0, 0)
        bottom_layout.addStretch()
        self.yes_button = QPushButton("Yes")
        self.yes_button.setProperty("status", "important")
        self.yes_button.setMinimumWidth(80)
        bottom_layout.addWidget(self.yes_button)
        self.no_button = QPushButton("No")
        self.no_button.setMinimumWidth(80)
        bottom_layout.addWidget(self.no_button)

    def setup_signals(self):
        self.yes_button.clicked.connect(self.yes_button_clicked)
        self.no_button.clicked.connect(self.no_button_clicked)

    def yes_button_clicked(self):
        self.confirmed.emit()

    def no_button_clicked(self):
        self.rejected.emit()


def setup_demo_project():
    # Download from github
    url = "https://github.com/bigcompany-public/bluepepper_demo_project/archive/refs/heads/main.zip"
    bluepepper_root = Path(os.environ["BLUEPEPPER_ROOT"])
    zip_file = bluepepper_root.parent.joinpath("tmp.zip")
    urllib.request.urlretrieve(url, zip_file)

    # Unzip
    unzip_dir = zip_file.parent.joinpath("tmp")
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(unzip_dir)

    # rename
    src = list(unzip_dir.iterdir())[0]
    project_root = Path(codex.convs.project_root.format())
    shutil.move(src, project_root)

    # clear temp files
    zip_file.unlink()
    shutil.rmtree(unzip_dir)

    # Load database dump
    database_dump_file = project_root / "database_dump.json"
    database.restore_database_dump(database_dump_file)


def show_dialog():
    app = get_qt_app()  # noqa: F841
    icon = qtawesome.icon("ri.settings-4-fill", scale_factor=1.35, color="#45AB9E")

    widget = DemoProjectWidget()
    container = ContainerWidget(widget=widget, title="Download Demo Project ?", icon=icon)
    dialog = ContainerDialog(container=container)
    widget.confirmed.connect(dialog.accept)
    widget.rejected.connect(dialog.reject)
    if dialog.exec():
        setup_demo_project()


if __name__ == "__main__":
    app = get_qt_app()
    show_dialog()
