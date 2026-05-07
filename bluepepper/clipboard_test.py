import base64
import logging
import sys
from io import BytesIO
from pathlib import Path

from PySide6.QtCore import QByteArray, QMimeData
from PySide6.QtWidgets import QApplication


def path_to_file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def build_windows_html_clipboard(html_fragment: str) -> bytes:
    """Wrap an HTML fragment in the Windows clipboard HTML format header."""
    MARKER = "Version:0.9\r\nStartHTML:{start_html:010d}\r\nEndHTML:{end_html:010d}\r\nStartFragment:{start_frag:010d}\r\nEndFragment:{end_frag:010d}\r\n"

    pre_fragment = "<html><body><!--StartFragment-->"
    post_fragment = "<!--EndFragment--></body></html>"

    dummy_header = MARKER.format(start_html=0, end_html=0, start_frag=0, end_frag=0)
    header_len = len(dummy_header.encode("utf-8"))

    pre_fragment_bytes = pre_fragment.encode("utf-8")
    fragment_bytes = html_fragment.encode("utf-8")
    post_fragment_bytes = post_fragment.encode("utf-8")

    start_html = header_len
    start_frag = header_len + len(pre_fragment_bytes)
    end_frag = start_frag + len(fragment_bytes)
    end_html = end_frag + len(post_fragment_bytes)

    header = MARKER.format(
        start_html=start_html,
        end_html=end_html,
        start_frag=start_frag,
        end_frag=end_frag,
    )

    return BytesIO(header.encode("utf-8") + pre_fragment_bytes + fragment_bytes + post_fragment_bytes).read()


def send_images_and_text_to_clipboard(
    paths: list[Path],
    caption: str | None = None,
    use_base64: bool = False,
):
    """
    use_base64: True  → embed image data directly (works in Notion, Slack, Electron apps)
                False → use file:// URIs (works in Word, LibreOffice, local browsers)
    """

    def img_src(p: Path) -> str:
        if use_base64:
            suffix = p.suffix.lower().lstrip(".")
            mime = "jpeg" if suffix == "jpg" else suffix
            data = base64.b64encode(p.read_bytes()).decode()
            return f"data:image/{mime};base64,{data}"
        return path_to_file_uri(p)

    image_tags = "".join(
        f'<img src="{img_src(p)}" alt="{p.name}"><br>'
        for p in paths
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
    )
    html_fragment = f"{image_tags}<p>{caption}</p>" if caption else image_tags

    logging.info(f"Sending {len(paths)} image(s) to clipboard (base64={use_base64})")

    windows_html = build_windows_html_clipboard(html_fragment)

    _ = QApplication.instance() or QApplication(sys.argv)
    mime_data = QMimeData()
    mime_data.setData("text/html", QByteArray(windows_html))
    if caption:
        mime_data.setText(caption)

    QApplication.clipboard().setMimeData(mime_data)


if __name__ == "__main__":
    paths = [Path(r"D:\gitWorkspace\BP_PROJECT_DEV\bluepepper\bluepepper\gui\icons\aquarium.png")]
    caption = "text so submit"
    send_images_and_text_to_clipboard(paths, caption)
