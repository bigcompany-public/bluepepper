import argparse
import logging
import sys
from pathlib import Path

from qtpy.QtCore import QMimeData, QUrl
from qtpy.QtWidgets import QApplication

from bluepepper.core import init_logging


def clear_clipboard():
    _ = QApplication.instance() or QApplication(sys.argv)
    clipboard = QApplication.clipboard()
    logging.info("Clearing clipboard")
    clipboard.clear(mode=clipboard.Mode.Clipboard)


def send_text_to_clipboard(text: str):
    short_text = text[:300] + "..." if len(text) > 300 else text
    logging.info(f"Sending text to clipboard:\n{short_text}")
    _ = QApplication.instance() or QApplication(sys.argv)
    clipboard = QApplication.clipboard()
    clipboard.setText(text, mode=clipboard.Mode.Clipboard)


def send_paths_to_clipboard(paths: list[Path]):
    paths = [Path(path) for path in paths]
    text = "\n".join([f"  - {path.name}" for path in paths])
    short_text = text[:300] + "..." if len(text) > 300 else text
    logging.info(f"Sending files to clipboard:\n{short_text}")
    _ = QApplication.instance() or QApplication(sys.argv)
    mime_data = QMimeData()
    urls = [QUrl.fromLocalFile(path) for path in paths]
    mime_data.setUrls(urls)
    clipboard = QApplication.clipboard()
    clipboard.setMimeData(mime_data)


if __name__ == "__main__":
    init_logging("clipboard")
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clear", action="store_true")
    parser.add_argument("-t", "--text", required=False)
    parser.add_argument("-p", "--path", required=False)
    args = parser.parse_args()

    if args.clear:
        clear_clipboard()
    if args.text:
        send_text_to_clipboard(args.text)
    elif args.path:
        send_paths_to_clipboard([args.path])
