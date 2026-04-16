from conf.app_browser import get_tool_config
from qtpy.QtWidgets import QApplication, QDialog, QVBoxLayout, QWidget

from bluepepper.tools.browser.browser_widget import BrowserWidget


class MainAppBrowserWidget(BrowserWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, get_tool_config())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = QDialog()
    layout = QVBoxLayout(dialog)
    browser_widget = MainAppBrowserWidget(parent=dialog)
    dialog.show()
    sys.exit(app.exec_())
