"""Console management for bluepepper pipeline."""

import win32con
import win32console
import win32gui


class BluePepperConsole:
    """Manager for showing/hiding the system console window."""

    def __init__(self) -> None:
        """Initialize console manager and get window handle."""
        self._hwnd: int | None = win32console.GetConsoleWindow() or None

    @property
    def window_handler(self) -> int | None:
        """Return the console window handle (None if unavailable)."""
        return self._hwnd

    @property
    def is_visible(self) -> bool:
        """Return True if the console window is currently visible."""
        return bool(self._hwnd and win32gui.IsWindowVisible(self._hwnd))

    def show(self) -> None:
        """Show the console window and bring it to the foreground.

        Uses a minimize→restore sequence to bypass the Windows 11
        foreground-lock restriction that causes SetForegroundWindow to
        raise error (0, …, 'No error message is available').
        """
        if not self._hwnd:
            return
        # Restore if minimised/hidden first so the window is on-screen.
        win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)

        # Minimize then restore — this makes our process the last to
        # receive a window event, satisfying Windows' foreground rules.
        win32gui.ShowWindow(self._hwnd, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self._hwnd)

    def hide(self) -> None:
        """Hide the console window."""
        if not self._hwnd:
            return
        win32gui.ShowWindow(self._hwnd, win32con.SW_HIDE)

    def toggle(self) -> None:
        """Toggle console visibility."""
        if not self._hwnd:
            return
        if self.is_visible:
            self.hide()
        else:
            self.show()

    def disable_exit_menu(self) -> None:
        """Remove the close button from the console window menu."""
        if not self._hwnd:
            return
        menu = win32gui.GetSystemMenu(self._hwnd, 0)
        try:
            win32gui.DeleteMenu(menu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
        except Exception:
            pass  # Menu item may already be absent.


def toggle_console() -> None:
    """Toggle console visibility (module-level convenience function)."""
    BluePepperConsole().toggle()


if __name__ == "__main__":
    BluePepperConsole().show()
