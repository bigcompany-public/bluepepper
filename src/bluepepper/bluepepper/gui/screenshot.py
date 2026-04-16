import logging
import sys

from bluepepper.core import get_temp_path, init_logging
from bluepepper.temp import get_temp_path
from qtpy.QtCore import QPoint, QRect, QSize, Qt
from qtpy.QtGui import QGuiApplication, QMouseEvent, QPainter, QPixmap
from qtpy.QtWidgets import QApplication, QDialog, QRubberBand, QVBoxLayout, QWidget


class Screenshot(QDialog):
    def __init__(self):
        super().__init__()

        # Create transparent frameless window
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Create semi-transparent widget on which the QRubberBand selection can be drawn
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.main_widget = QWidget()
        self.main_layout.addWidget(self.main_widget)
        self.main_widget.setStyleSheet("background-color: rgba(255, 255, 255, 50);")

        # Resize to cover all screens
        geo = QApplication.primaryScreen().virtualGeometry()
        self.setGeometry(geo)

        # Initialize QRubberBand
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.setMouseTracking(True)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Start rubber band selection on mouse press."""
        self.origin = event.pos()
        self.rubberband.setGeometry(QRect(self.origin, QSize()))
        self.rubberband.show()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Update rubber band geometry during mouse movement."""
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if not self.rubberband.isVisible():
            super().mouseReleaseEvent(event)
            return

        self.rubberband.hide()
        rect = self.rubberband.geometry()

        # do nothing if the selection was too small
        if rect.width() < 10 and rect.height() < 10:
            super().mouseReleaseEvent(event)
            return

        # Hide overlay before capture
        self.hide()
        QApplication.processEvents()

        screenshot = self.capture_region(rect)
        path = get_temp_path("screenshot").with_suffix(".png")
        path.parent.mkdir(exist_ok=True, parents=True)
        screenshot.save(path.as_posix())
        logging.info(f"Saved screenshot to {path}")

        # Re-show the widget, otherwise the process hangs
        self.show()

        super().mouseReleaseEvent(event)
        self.close()

    def grab_full_virtual_desktop(self):
        """
        Capture all physical screens and stitch them into
        a single QPixmap matching virtualGeometry().
        """
        screens = QGuiApplication.screens()
        virtual_geo = QGuiApplication.primaryScreen().virtualGeometry()

        result = QPixmap(virtual_geo.size())
        result.fill(Qt.transparent)

        painter = QPainter(result)

        for screen in screens:
            geo = screen.geometry()
            pix = screen.grabWindow(0)

            # Offset inside the virtual desktop pixmap
            offset_x = geo.x() - virtual_geo.x()
            offset_y = geo.y() - virtual_geo.y()

            painter.drawPixmap(offset_x, offset_y, pix)

        painter.end()
        return result

    def capture_region(self, rect: QRect):
        """
        Capture the selected region from the virtual desktop.
        Using stitched multi-screen capture.
        """
        full = self.grab_full_virtual_desktop()
        return full.copy(rect)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)


def capture_screenshot():
    app = QApplication.instance() or QApplication(sys.argv)
    w = Screenshot()
    w.exec_()


if __name__ == "__main__":
    init_logging("screenshot")
    capture_screenshot()
