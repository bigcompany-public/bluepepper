from __future__ import annotations

import sys

import qtawesome as qta
from PySide6.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QRect, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from bluepepper.gui.utils import get_theme


class HelpMeButton(QWidget):
    """
    Responsive widghet designed to be visually appealing and coherent all across BluePepper
    Serves as the go-to button, when the user needs to open a ticket, or seek guidance
    """

    # Proportionality constants
    _ICON_RATIO = 0.8
    _FONT_RATIO = 0.45
    _MARGIN_RATIO = 0
    _EXPANDED_RATIO = 4.0

    # Colour palette
    theme = get_theme()
    colors = {
        "bg": theme["ok"],
        "text": "white",
        "icon_color": "white",
    }

    def __init__(self, size: int = 32, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._size = size
        self._derive_metrics()

        self.setFixedHeight(self._size)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Inner button
        self._btn = QPushButton(self)
        self._apply_style()
        self._set_icon()

        # Start collapsed
        self._btn.setGeometry(self._collapsed_rect())

        # Hover animation
        self._anim = QPropertyAnimation(self._btn, b"geometry")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        # Signal
        self._btn.clicked.connect(self._on_clicked)

        # Track hover on the inner button
        self._btn.installEventFilter(self)

    def _derive_metrics(self) -> None:
        """Recompute all size-dependent values from ``self._size``."""
        s = self._size
        self._margin = max(4, int(s * self._MARGIN_RATIO))
        self._collapsed_w = s  # square when collapsed
        self._expanded_w = int(s * self._EXPANDED_RATIO)
        self._icon_size = max(12, int(s * self._ICON_RATIO))
        self._font_pt = max(7, int(s * self._FONT_RATIO))
        self._radius = s // 2

        # Widget's minimum width guarantees full expansion fits inside
        self.setMinimumWidth(self._expanded_w + self._margin * 2)

    def _right_x(self, btn_width: int) -> int:
        """X coordinate that places *btn_width* flush with the right margin."""
        return max(0, self.width() - btn_width - self._margin)

    def _collapsed_rect(self) -> QRect:
        return QRect(
            self._right_x(self._collapsed_w),
            0,
            self._collapsed_w,
            self._size,
        )

    def _expanded_rect(self) -> QRect:
        return QRect(
            self._right_x(self._expanded_w),
            0,
            self._expanded_w,
            self._size,
        )

    def _apply_style(self) -> None:
        self._btn.setFixedHeight(self._size)
        self._btn.setFont(QFont("Segoe UI", self._font_pt))
        self._btn.setIconSize(QSize(self._icon_size, self._icon_size))
        self._btn.setContentsMargins(0, 0, 0, 0)
        _stylesheet = f"""
            QPushButton {{
                background-color: {self.colors["bg"]};
                font-weight: bold; color: {self.colors["text"]};
                border: none; border-radius: {self._radius}px;
                margin: 0px; padding: 0px;
            }}"""
        self._btn.setStyleSheet(_stylesheet)

    def _set_icon(self, with_text: bool = False) -> None:
        icon = qta.icon(
            "fa5s.hand-sparkles", scale_factor=1, color=self.colors["icon_color"]
        )
        self._btn.setIcon(icon)
        if with_text:
            self._btn.setText(" Help Me")
        else:
            self._btn.setText("")

    def resizeEvent(self, event) -> None:  # noqa: N802
        """Snap back to collapsed when the container is resized."""
        super().resizeEvent(event)
        self._anim.stop()
        self._btn.setGeometry(self._collapsed_rect())
        self._set_icon(with_text=False)

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        if watched is self._btn:
            if event.type() == QEvent.Enter:
                self._on_enter()
            elif event.type() == QEvent.Leave:
                self._on_leave()
        return super().eventFilter(watched, event)

    def _on_enter(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._collapsed_rect())
        self._anim.setEndValue(self._expanded_rect())
        self._anim.start()
        self._set_icon(with_text=True)

    def _on_leave(self) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._expanded_rect())
        self._anim.setEndValue(self._collapsed_rect())
        self._anim.start()
        self._set_icon(with_text=False)

    def _on_clicked(self) -> None:
        print("Help Me clicked")


if __name__ == "__main__":

    class MainWindow(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.resize(500, 300)
            self.setWindowTitle("Help Button Example")

            layout = QVBoxLayout(self)

            label = QLabel("A " * 1000)
            label.setWordWrap(True)
            layout.addWidget(label)

            layout.addWidget(HelpMeButton(size=128, parent=self))
            layout.addWidget(HelpMeButton(size=64, parent=self))
            layout.addWidget(HelpMeButton(size=32, parent=self))
            layout.addWidget(HelpMeButton(size=16, parent=self))

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
