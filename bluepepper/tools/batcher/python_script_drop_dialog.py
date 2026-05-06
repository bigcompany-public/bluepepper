from pathlib import Path
from typing import Any

from qtpy.QtCore import QEvent, Qt, Signal
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from bluepepper.gui.utils import get_icon, get_qt_app, get_qta_icon
from bluepepper.gui.widgets.container import ContainerDialog, ContainerWidget
from bluepepper.tools.batcher.job_model import JobData
from bluepepper.tools.browser.browser_widget import BrowserWidget, get_batcher_widget


class PythonDropWidget(QWidget):
    _accepted = Signal(Path)

    def __init__(self):
        super().__init__()
        self.path: Path | None = None
        self.setFixedSize(300, 300)
        popup_layout = QVBoxLayout(self)
        self.label = QLabel("Drop your python script here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        popup_layout.addWidget(self.label)
        frame = QFrame()
        frame.setProperty("depth", "2")
        popup_layout.addWidget(frame)
        py_frame_layout = QVBoxLayout(frame)
        drop_widget = QLabel()
        python_icon = QPixmap(get_icon("icon_python.svg"))
        drop_widget.setPixmap(
            python_icon.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )
        self.setAcceptDrops(True)
        py_frame_layout.addWidget(drop_widget, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter)

    def dragEnterEvent(self, event: QEvent):
        event.accept()

    def dragLeaveEvent(self, event: QEvent): ...

    def dropEvent(self, event: QEvent):
        event.accept()
        paths = event.mimeData().urls()
        if len(paths) != 1:
            raise RuntimeError("Please provide only one python script")

        path = Path(paths[0].toLocalFile())
        if path.suffix != ".py":
            raise TypeError("Only .py files are accepted")

        self.path = path
        self._accepted.emit(path)


def prompt_for_python_script() -> Path | None:
    app = get_qt_app()
    icon = get_qta_icon(name="mdi6.language-python", scale_factor=1.25, color="#306998")
    widget = PythonDropWidget()
    container = ContainerWidget(widget=widget, icon=icon, title="Batch Python Script")
    dialog = ContainerDialog(container)
    widget._accepted.connect(dialog.accept)
    if dialog.exec():
        return widget.path


def add_jobs(browser: BrowserWidget, targets: list[Any]) -> None:
    script_path = prompt_for_python_script()
    if not script_path:
        return

    batcher = get_batcher_widget(browser)
    for target in targets:
        job_data = JobData(
            name=f"Python Script - {target}",
            description="Exectuting custom python script",
            script_path=script_path,
            script_args=[target],
        )
        batcher.add_job(job_data)


if __name__ == "__main__":
    print(prompt_for_python_script())
