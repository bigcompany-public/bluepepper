from __future__ import annotations

import math

import qtawesome
from bluepepper.gui.utils import stylesheet
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from qtpy.QtCore import QEvent, QPointF, Qt, QTimer, Signal
from qtpy.QtGui import QColor, QImage, QPainter, QPainterPath, QPen
from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)


def _normalize_hex(text: str) -> str | None:
    """
    Accept hex strings with or without '#', upper or lower case.
    Returns a canonical '#RRGGBB' string, or None if the value is invalid.
    """
    text = text.strip()
    if not text.startswith("#"):
        text = "#" + text
    color = QColor(text.upper())
    return color.name().upper() if color.isValid() else None


def _hex_to_qcolor(hex_color: str) -> QColor:
    """Convert a canonical '#RRGGBB' hex string to a QColor."""
    return QColor(hex_color)


def _qcolor_to_hex(qcolor: QColor) -> str:
    """Convert a QColor to a canonical '#RRGGBB' hex string."""
    return qcolor.name().upper()


class HexLineEdit(QLineEdit):
    """
    A QLineEdit specialised for hex color input.

    - Accepts values with or without '#', in any case.
    - Pressing Enter validates the input and applies the color; it does NOT
      propagate the key event so it cannot accidentally close a parent dialog.
    - If the entered value is invalid, the field reverts to the last known
      good value (shown with a brief red-border flash).
    - Emits ``colorCommitted(str)`` with the canonical '#RRGGBB' value when
      the user successfully commits a new color via Enter.
    """

    colorCommitted = Signal(str)  # emits canonical '#RRGGBB' hex string

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_valid_hex: str = "#000000"

    def set_last_valid_hex(self, hex_color: str):
        """Keep the internal fallback in sync with external set_hex_color calls."""
        self._last_valid_hex = hex_color

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._commit()
            # Consume the event so it never reaches the dialog's button-box
            event.accept()
            return
        super().keyPressEvent(event)

    def _commit(self):
        canonical_hex = _normalize_hex(self.text())
        if canonical_hex is None:
            # Invalid — flash red border and revert
            self.setStyleSheet("border: 1px solid red;")
            self.setText(self._last_valid_hex)
            # Restore normal stylesheet after a short delay
            QTimer.singleShot(600, lambda: self.setStyleSheet(""))
            return

        self._last_valid_hex = canonical_hex
        self.setText(canonical_hex)
        self.colorCommitted.emit(canonical_hex)


class ColorWheel(QWidget):
    colorChanged = Signal(str)  # emits canonical '#RRGGBB' hex string

    def __init__(self, diameter: int = 200, start_color: str = "#FFFFFF"):
        super().__init__()
        self.margin = 6
        self.wheel_diameter = diameter
        widget_size = diameter + self.margin * 2
        self.setFixedSize(widget_size, widget_size)
        self.radius = diameter / 2

        # wheel centre in widget coords
        self.cx = widget_size / 2
        self.cy = widget_size / 2

        self.hue = 0
        self.saturation = 0
        self.value = 255

        self._cursor = (self.cx, self.cy)

        self._generate_wheel()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.set_hex_color(start_color)

    def _generate_wheel(self):
        size = self.wheel_diameter
        self.base = QImage(size, size, QImage.Format_ARGB32)
        r = self.radius

        for y in range(size):
            for x in range(size):
                dx = x - r
                dy = y - r
                dist = math.sqrt(dx * dx + dy * dy)

                if dist <= r:
                    angle = (math.degrees(math.atan2(dx, dy)) + 180) % 360
                    sat = dist / r
                    c = QColor()
                    c.setHsv(int(angle), int(sat * 255), 255)
                    self.base.setPixelColor(x, y, c)
                else:
                    self.base.setPixelColor(x, y, QColor(0, 0, 0, 0))

    def get_qcolor(self) -> QColor:
        """Return the current color as a QColor."""
        qcolor = QColor()
        qcolor.setHsv(int(self.hue), int(self.saturation), int(self.value))
        return qcolor

    def get_hex_color(self) -> str:
        """Return the current color as a canonical '#RRGGBB' hex string."""
        return _qcolor_to_hex(self.get_qcolor())

    def set_value(self, value: int):
        self.value = value
        self.colorChanged.emit(self.get_hex_color())
        self.update()

    def set_hex_color(self, hex_color: str):
        """Set the wheel state from a '#RRGGBB' hex color string."""
        qcolor = _hex_to_qcolor(hex_color)
        if not qcolor.isValid():
            return

        h, s, v, _ = qcolor.getHsv()  # type: ignore
        self.hue = h if h >= 0 else 0
        self.saturation = s
        self.value = v

        # Recompute cursor position from hue/saturation
        angle_rad = math.radians(self.hue - 180)
        dist = (self.saturation / 255) * self.radius
        cursor_x = self.cx + dist * math.sin(angle_rad)
        cursor_y = self.cy + dist * math.cos(angle_rad)
        self._cursor = (cursor_x, cursor_y)

        self.colorChanged.emit(self.get_hex_color())
        self.update()

    def mousePressEvent(self, event: QEvent):
        self._pick(event.x(), event.y())

    def mouseMoveEvent(self, event):
        if event.buttons():
            self._pick(event.x(), event.y())

    def _pick(self, x: int, y: int):
        dx = x - self.cx
        dy = y - self.cy
        dist = math.sqrt(dx * dx + dy * dy)

        # clamp to circle edge
        if dist > self.radius:
            scale = self.radius / dist
            x = self.cx + dx * scale
            y = self.cy + dy * scale
            dist = self.radius

        angle = (math.degrees(math.atan2(dx, dy)) + 180) % 360
        sat = min(255, int((dist / self.radius) * 255))

        self.hue = angle
        self.saturation = sat
        self._cursor = (x, y)

        self.colorChanged.emit(self.get_hex_color())
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        # Create darkened image wheel
        img = QImage(self.base)
        darkness = 1 - (self.value / 255)

        if darkness > 0:
            painter = QPainter(img)
            painter.setCompositionMode(QPainter.CompositionMode_Multiply)
            painter.fillRect(img.rect(), QColor(0, 0, 0, int(darkness * 255)))
            painter.end()

        # clip painter to the wheel circle before drawing the image
        path = QPainterPath()
        path.addEllipse(QPointF(self.cx, self.cy), self.radius, self.radius)
        p.setClipPath(path)
        p.drawImage(self.margin, self.margin, img)
        p.setClipping(False)

        # smooth anti-aliased outline drawn outside the wheel pixels
        pen = QPen(QColor(80, 80, 80), 1.5)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(self.cx, self.cy), self.radius, self.radius)

        # cursor
        pen = QPen(QColor("white"), 2)
        p.setPen(pen)
        p.drawEllipse(QPointF(*self._cursor), 5, 5)


class BrightnessSlider(QSlider):
    def __init__(self) -> None:
        super().__init__(Qt.Vertical)
        self.setRange(0, 255)
        self.setValue(255)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))

    def set_hex_color(self, hex_color: str):
        """Set slider brightness from a '#RRGGBB' hex color string."""
        qcolor = _hex_to_qcolor(hex_color)
        if not qcolor.isValid():
            return
        _, _, v, _ = qcolor.getHsv()
        # Block signals to avoid feedback loops; the ColorPicker
        # orchestrates all updates from the wheel's colorChanged signal.
        self.blockSignals(True)
        self.setValue(v)
        self.blockSignals(False)


class ColorPreview(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedHeight(40)

    def set_hex_color(self, hex_color: str):
        """Update the preview swatch from a '#RRGGBB' hex color string."""
        qcolor = _hex_to_qcolor(hex_color)
        if not qcolor.isValid():
            return
        self.setStyleSheet(
            f"background:{hex_color};border:1px solid black;border-radius:8px;"
        )


class ColorPicker(QWidget):
    colorChanged = Signal(str)  # emits canonical '#RRGGBB' hex string

    def __init__(self, wheel_diameter: int = 200, start_color: str = "#FFFFFF"):
        super().__init__()
        self._wheel_diameter = wheel_diameter
        self._start_color = start_color
        self.setStyleSheet(stylesheet)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Color Picker")
        self.wheel = ColorWheel(self._wheel_diameter, self._start_color)
        self.slider = BrightnessSlider()
        slider_container = QWidget()
        slider_layout = QVBoxLayout()
        slider_container.setLayout(slider_layout)
        slider_layout.setContentsMargins(0, 20, 0, 20)
        slider_layout.addWidget(self.slider)
        self.preview = ColorPreview()
        self.hex = HexLineEdit()
        self.hex.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.preview.setFixedHeight(self.hex.sizeHint().height())

        parent_layout = QVBoxLayout()
        self.setLayout(parent_layout)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        parent_widget = QWidget()
        parent_layout.addWidget(parent_widget)

        main_layout = QVBoxLayout()
        parent_widget.setLayout(main_layout)
        parent_widget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        top_widget = QWidget()
        main_layout.addWidget(top_widget)
        main_layout.setContentsMargins(3, 3, 3, 3)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_widget.setLayout(top_layout)
        top_layout.addWidget(self.wheel)
        top_widget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        top_layout.addWidget(slider_container)

        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_widget.setLayout(bottom_layout)
        bottom_layout.addWidget(self.preview)
        bottom_layout.addWidget(self.hex)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(bottom_widget)

        self.slider.valueChanged.connect(self.wheel.set_value)
        self.wheel.colorChanged.connect(self._on_wheel_hex_color_changed)
        self.hex.colorCommitted.connect(self.set_hex_color)

        self.slider.set_hex_color(self._start_color)
        self._update_ui(self.wheel.get_hex_color())

    def _on_wheel_hex_color_changed(self, hex_color: str):
        """Internal handler: sync all child widgets then re-emit colorChanged."""
        self._update_ui(hex_color)
        self.colorChanged.emit(hex_color)

    def _update_ui(self, hex_color: str):
        self.preview.set_hex_color(hex_color)
        self.hex.setText(hex_color)
        self.hex.set_last_valid_hex(hex_color)

    def set_hex_color(self, hex_color: str):
        """
        Set the picker to the given hex color.
        Propagates to the wheel (which re-emits colorChanged,
        triggering _update_ui) and to the brightness slider.
        """
        self.slider.set_hex_color(hex_color)  # sync slider first (no signal)
        self.wheel.set_hex_color(hex_color)  # wheel emits colorChanged -> _update_ui

    def get_hex_color(self) -> str:
        """Return the current color as a canonical '#RRGGBB' hex string."""
        return self.wheel.get_hex_color()

    def get_qcolor(self) -> QColor:
        """Return the current color as a QColor."""
        return self.wheel.get_qcolor()


class ColorPickerWithButtons(QWidget):
    colorChanged = Signal(str)  # emits canonical '#RRGGBB' hex string

    def __init__(self, wheel_diameter: int = 200, start_color: str = "#FFFFFF") -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.color_picker = ColorPicker(wheel_diameter, start_color)
        layout.addWidget(self.color_picker)

        self.ok_button = QPushButton("OK")
        self.ok_button.setProperty("status", "important")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)

        # Bubble up colorChanged from the inner picker
        self.color_picker.colorChanged.connect(self.colorChanged)

    def set_hex_color(self, hex_color: str):
        """Delegate to the inner ColorPicker."""
        self.color_picker.set_hex_color(hex_color)

    def get_hex_color(self) -> str:
        """Return the current color as a canonical '#RRGGBB' hex string."""
        return self.color_picker.get_hex_color()

    def get_qcolor(self) -> QColor:
        """Return the current color as a QColor."""
        return self.color_picker.get_qcolor()


def pick_color(
    wheel_diameter: int = 200,
    start_color: str = "#FFFFFF",
    on_color_changed=None,
) -> str | None:
    """
    Open the color-picker dialog.

    Parameters
    ----------
    wheel_diameter : int
        Diameter of the color wheel in pixels.
    start_color : str | None
        Optional hex color (e.g. '#FF8800') to pre-select when the dialog opens.
    on_color_changed : callable | None
        Optional callback(hex_color: str) connected to the colorChanged signal.
        Defaults to printing the selected hex value to stdout.

    Returns
    -------
    str | None
        The selected hex color if the user pressed OK, otherwise None.
    """
    app = get_qt_app()
    widget = ColorPickerWithButtons(wheel_diameter, start_color)
    icon = qtawesome.icon("ph.eyedropper-fill", scale_factor=1.35, color="#1E69FF")
    container = ContainerWidget(widget, title="ColorWheel", icon=icon)
    dialog = ContainerDialog(container)
    size = widget.sizeHint()
    dialog.setFixedSize(size.width(), size.height())
    widget.ok_button.clicked.connect(dialog.accept)

    # Connect colorChanged signal
    if on_color_changed is not None:
        widget.colorChanged.connect(on_color_changed)

    if dialog.exec():
        return widget.get_hex_color()


if __name__ == "__main__":
    color = pick_color(300, start_color="#5574B3")
    print(color)
