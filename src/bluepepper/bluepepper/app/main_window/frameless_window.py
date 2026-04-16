import ctypes
import sys
from ctypes import wintypes

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QLabel, QMainWindow

# win32 constants
GWL_STYLE = -16
WS_THICKFRAME = 0x00040000
WM_NCCALCSIZE = 0x0083
WM_NCACTIVATE = 0x0086
WM_NCHITTEST = 0x0084
HTCLIENT = 1
HTCAPTION = 2
HTLEFT = 10
HTRIGHT = 11
HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOM = 15
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17

user32 = ctypes.windll.user32


class FramelessMainWindow(QMainWindow):
    """
    Frameless window with:
    - Win+Arrow snapping (left/right/up/down)
    - Edge resizing
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(1200, 700)
        self.setWindowFlags(
            # Hides default frame
            Qt.FramelessWindowHint
            |
            # Allows win+up to maximize and win+down to minimize
            Qt.WindowMinMaxButtonsHint
        )
        self._activate_window_resizing()

    def _activate_window_resizing(self):
        """
        Re-add styles that Qt removes with FramelessWindowHint so Windows
        still treats the window as resizable (which re-enables both the resize handles and Win+Arrow snapping).
        However, this causes the widget to be wierdly cropped, so the nativeEvent is added to properly
        handle redraw
        """
        hwnd = wintypes.HWND(int(self.winId()))
        style = user32.GetWindowLongW(hwnd, GWL_STYLE)
        style |= WS_THICKFRAME
        user32.SetWindowLongW(hwnd, GWL_STYLE, style)

    def nativeEvent(self, eventType, message):
        # eventType for Qt on Windows is "windows_generic_MSG"
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(int(message))
            m = msg.message
            # WM_NCCALCSIZE: adjust client area. We handle it and return 0 (no redraw flag).
            if m == WM_NCCALCSIZE:
                # Important: returning 0 tells Windows we handled it and avoids extra non-client redraws.
                # Do NOT return WVR_REDRAW here (that caused the flash)
                return True, 0

            # WM_NCACTIVATE: prevent default non-client (titlebar) painting when active/inactive changes.
            # Returning a nonzero value tells Windows we've handled activation and it shouldn't draw caption.
            if m == WM_NCACTIVATE:
                return True, 1

            # WM_NCHITTEST: let Windows know where the mouse is for resizing (so WS_THICKFRAME actually works).
            if m == WM_NCHITTEST:
                # lParam low/high words are screen coords of mouse
                lparam = msg.lParam
                x = ctypes.c_short(lparam & 0xFFFF).value
                y = ctypes.c_short((lparam >> 16) & 0xFFFF).value

                # get window rect
                hwnd = wintypes.HWND(int(self.winId()))
                rect = wintypes.RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom

                # border width (in pixels) to consider for resizing area
                border = 8

                # compute distances
                on_left = x >= left and x < left + border
                on_right = x < right and x >= right - border
                on_top = y >= top and y < top + border
                on_bottom = y < bottom and y >= bottom - border

                # corners
                if on_top and on_left:
                    return True, HTTOPLEFT
                if on_top and on_right:
                    return True, HTTOPRIGHT
                if on_bottom and on_left:
                    return True, HTBOTTOMLEFT
                if on_bottom and on_right:
                    return True, HTBOTTOMRIGHT
                if on_left:
                    return True, HTLEFT
                if on_right:
                    return True, HTRIGHT
                if on_top:
                    return True, HTTOP
                if on_bottom:
                    return True, HTBOTTOM

                # otherwise client area (so we can still receive mouse events)
                return True, HTCLIENT

        return False, 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FramelessMainWindow()
    w.setWindowTitle("Frameless Main Window")
    label = QLabel("Hello world")
    label.setStyleSheet("background-color:#99BBAA; border: 5px solid red")
    w.setCentralWidget(label)
    w.show()
    sys.exit(app.exec())
