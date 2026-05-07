import argparse
import base64
import logging
import mimetypes
import sys
from pathlib import Path

from PySide6.QtGui import QImage
from qtpy.QtCore import QByteArray, QMimeData, QUrl
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


def send_rich_to_clipboard(html: str, plain_text: str | None = None):
    """
    html: full HTML string, images can be remote URLs or base64 data URIs
    """
    logging.info("Sending rich HTML content to clipboard")
    _ = QApplication.instance() or QApplication(sys.argv)

    mime_data = QMimeData()
    mime_data.setHtml(html)
    if plain_text:
        mime_data.setText(plain_text)

    QApplication.clipboard().setMimeData(mime_data)


def image_to_data_uri(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    mime = "jpeg" if suffix == "jpg" else suffix  # image/jpeg not image/jpg
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/{mime};base64,{data}"


def send_images_as_rich_clipboard(paths: list[Path], caption: str | None = None):
    paths = [Path(path) for path in paths]
    image_tags = "".join(
        f'<img src="{image_to_data_uri(p)}" alt="{p.name}"><br>'
        for p in paths
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
    )
    html = f"{image_tags}<p>{caption}</p>" if caption else image_tags

    plain = caption or ""

    send_rich_to_clipboard(html, plain)


def inspect_clipboard():
    app = QApplication.instance() or QApplication(sys.argv)
    clipboard = QApplication.clipboard()
    mime_data: QMimeData = clipboard.mimeData()

    print("=== Clipboard Inspection ===\n")
    print(f"Available MIME formats: {mime_data.formats()}\n")

    # --- Text ---
    if mime_data.hasText():
        print("[ TEXT ]")
        print(repr(mime_data.text()))
        print()

    # --- HTML ---
    if mime_data.hasHtml():
        print("[ HTML ]")
        print(mime_data.html())
        print()

    # --- URLs ---
    if mime_data.hasUrls():
        print("[ URLs ]")
        for url in mime_data.urls():
            print(f"  {url.toString()}")
        print()

    # --- Image ---
    if mime_data.hasImage():
        from PySide6.QtGui import QImage

        image = mime_data.imageData()
        if isinstance(image, QImage) and not image.isNull():
            print("[ IMAGE ]")
            print(f"  Size   : {image.width()} x {image.height()} px")
            print(f"  Format : {image.format()}")
            print(f"  Depth  : {image.depth()} bit")
            print(f"  DPI    : {image.dotsPerMeterX() / 39.37:.0f} x {image.dotsPerMeterY() / 39.37:.0f}")
            print()

    # --- Raw bytes for every format ---
    print("[ RAW BYTES PER FORMAT ]")
    for fmt in mime_data.formats():
        raw = mime_data.data(fmt)
        size = len(raw)
        preview = bytes(raw[:64]).hex()
        print(f"  {fmt!r:50s}  {size:6d} bytes  first 64 bytes: {preview}")

    print("\n=== Done ===")


def send_stuff_to_clipboard(
    text: str | None = None,
    files: list[str | Path] | None = None,
):
    """
    Send text and/or files to the clipboard.

    Args:
        text:   Any plain string (optional).
        files:  List of file paths. Each file is added under its MIME type.
                Images are also set as the clipboard image (hasImage() = True).
    """
    app = QApplication.instance() or QApplication(sys.argv)
    mime = QMimeData()

    # ── Text ──────────────────────────────────────────────────────────────
    if text is not None:
        mime.setText(text)

    # ── Files ─────────────────────────────────────────────────────────────
    if files:
        urls = []
        for raw_path in files:
            path = Path(raw_path).resolve()
            if not path.exists():
                raise FileNotFoundError(path)

            mime_type, _ = mimetypes.guess_type(str(path))
            mime_type = mime_type or "application/octet-stream"

            raw_bytes = path.read_bytes()

            # 1. Always add as raw bytes under its MIME type
            mime.setData(mime_type, QByteArray(raw_bytes))

            # 2. If it's an image, also set it as a QImage so hasImage() works
            if mime_type.startswith("image/"):
                img = QImage()
                img.loadFromData(QByteArray(raw_bytes))
                if not img.isNull():
                    mime.setImageData(img)

            # 3. Register as a file URL (so hasUrls() works — useful for
            #    file managers, IDEs, etc. that paste by URL)
            urls.append(QUrl.fromLocalFile(str(path)))

        mime.setUrls(urls)

    QApplication.clipboard().setMimeData(mime)

    # ── Summary ───────────────────────────────────────────────────────────
    print("✓ Clipboard updated.")
    print(f"  formats : {mime.formats()}")
    if mime.hasText():
        print(f"  text    : {mime.text()!r}")
    if mime.hasUrls():
        print(f"  urls    : {[u.toString() for u in mime.urls()]}")
    if mime.hasImage():
        img = mime.imageData()
        print(f"  image   : {img.width()}x{img.height()} px")


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
        send_stuff_to_clipboard(args.text, [args.path, args.path])
    elif args.text:
        send_text_to_clipboard(args.text)
    elif args.path:
        send_paths_to_clipboard([args.path])
