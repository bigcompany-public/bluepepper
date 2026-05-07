import argparse
import base64
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


def image_to_data_uri(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    mime = "jpeg" if suffix == "jpg" else suffix
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/{mime};base64,{data}"


def send_html_to_clipboard(paragraphs: list[str | Path]):
    _ = QApplication.instance() or QApplication(sys.argv)
    clipboard = QApplication.clipboard()
    logging.info("Clearing clipboard")
    clipboard.clear(mode=clipboard.Mode.Clipboard)

    mime_data = QMimeData()
    html_lines = ["<html>", "<body>", "<!--StartFragment-->"]
    for paragraph in paragraphs:
        if isinstance(paragraph, str):
            html_lines.append(f"<p>{paragraph}</p>")
        elif isinstance(paragraph, Path):
            html_lines.append(f'<p><img src="{image_to_data_uri(paragraph)}" alt="image"></p>')

    html_lines += ["<!--EndFragment-->", "</body>", "</html>"]
    html = "\n".join(html_lines)
    mime_data.setHtml(html)
    clipboard = QApplication.clipboard()
    clipboard.setMimeData(mime_data)


def inspect_clipboard():
    app = QApplication.instance() or QApplication(sys.argv)
    clipboard = QApplication.clipboard()
    mime_data: QMimeData = clipboard.mimeData()

    print("=== Clipboard Inspection ===\n")
    print(f"Available MIME formats: {mime_data.formats()}\n")

    if mime_data.hasText():
        print()
        print("[ TEXT ]")
        print(repr(mime_data.text()))

    if mime_data.hasHtml():
        print()
        print("[ HTML ]")
        print(mime_data.html())

    if mime_data.hasUrls():
        print()
        print("[ URLs ]")
        for url in mime_data.urls():
            print(f"  {url.toString()}")


if __name__ == "__main__":
    init_logging("clipboard")
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clear", action="store_true")
    parser.add_argument("-i", "--inspect", action="store_true")
    parser.add_argument("-t", "--text", required=False)
    parser.add_argument("-p", "--path", required=False)
    args = parser.parse_args()

    if args.clear:
        clear_clipboard()
    elif args.inspect:
        inspect_clipboard()
    elif args.path and args.text:
        paragraphs = [args.text, Path(args.path)]
        send_html_to_clipboard(paragraphs)
    elif args.text:
        send_text_to_clipboard(args.text)
    elif args.path:
        send_paths_to_clipboard([args.path])
