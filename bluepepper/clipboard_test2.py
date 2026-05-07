import logging
import sys
from pathlib import Path

from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QApplication
from qtpy.QtCore import QMimeData

from bluepepper.core import init_logging


def send_images_and_text_to_clipboard(paths: list[Path], text: str):
    _ = QApplication.instance() or QApplication(sys.argv)
    clipboard = QApplication.clipboard()
    logging.info("Clearing clipboard")
    clipboard.clear(mode=clipboard.Mode.Clipboard)

    mime_data = QMimeData()
    mime_data.setHtml
    clipboard = QApplication.clipboard()
    clipboard.setMimeData(mime_data)


if __name__ == "__main__":
    init_logging("sandbox")
    paths = [Path(r"D:\gitWorkspace\BP_PROJECT_DEV\bluepepper\bluepepper\gui\icons\aquarium.png")]
    caption = "text so submit"
    send_images_and_text_to_clipboard(paths, caption)
