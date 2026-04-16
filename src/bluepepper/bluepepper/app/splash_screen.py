import logging
import os
import shutil
import sys
import traceback
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path

from install.install import BluePepperInstaller
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QColor, QFont, QPainter, QPixmap
from qtpy.QtWidgets import QApplication, QSplashScreen

from bluepepper.console import BluePepperConsole
from bluepepper.core import init_logging, root_dir
from bluepepper.gui.widgets.outcome_popups import show_error


def except_hook(exc_type, exc_value, exc_traceback):
    console = BluePepperConsole()
    console.show()
    formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
    formatted_traceback = "".join(formatted_traceback)
    logging.error(formatted_traceback)
    show_error(error=str(exc_value), traceback=formatted_traceback)
    sys.exit(1)


def show_splash_screen(update: bool = False) -> bool:
    """Returns whether or not the update was successful"""
    init_logging("bluepepperAppStartup")

    # Setup a hook that forces the console to show + an error widget
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    splash = BluePepperSplash(update)
    splash.show()
    splash.run_tasks()
    app.exec()
    return splash.success


class BluePepperSplash(QSplashScreen):
    def __init__(self, update: bool = False):
        # Static texts
        self.app_name = "BluePepper"
        self.credits = "Big Company\nCode by Tristan Languebien\nArtwork by Rohan Dalvi"

        # Dynamic status text
        self.status = "Loading..."
        self.status_font = QFont("Segoe UI", 12)
        self.status_color = QColor("#0C192C")

        self.root_dir = Path(os.environ["BLUEPEPPER_ROOT"])
        self.success = True
        self._update = update
        self.installer = BluePepperInstaller()
        path = root_dir / "bluepepper/gui/img/splashscreen.png"
        pixmap = QPixmap(path.as_posix())
        super().__init__(pixmap)

        # Make the slash screen appear on top without using the Qt.WindowStaysOnTopHint flag
        # which causes a top bar to appear on the splash screen
        self.showMinimized()
        self.showNormal()

    def set_status(self, text):
        """Update the status text and repaint."""
        self.status = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # App name
        rect = self.rect().adjusted(20, -40, -20, -20)
        painter.setPen(QColor("#0C192C"))
        painter.setFont(QFont("Segoe UI", 24, QFont.Bold))
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignBottom, self.app_name)

        # Credits
        rect = self.rect().adjusted(0, 0, -10, -10)
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(rect, Qt.AlignRight | Qt.AlignBottom, self.credits)

        # Dynamic status
        rect = self.rect().adjusted(150, -40, -20, -23)
        painter.setPen(self.status_color)
        painter.setFont(self.status_font)
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignBottom, self.status)

    def update_venvs(self):
        if self._update:
            self.installer.setup_virtual_environments()

    def connect_to_mongodb_server(self):
        from bluepepper.core import database

        # make a siple query to test the connection
        database.assets.find_one()

    def toggle_console(self):
        if not int(os.environ["BLUEPEPPER_CONSOLE"]):
            console = BluePepperConsole()
            console.hide()

    def fetch_version(self):
        if self._update:
            self.installer.fetch_current_tag()

    def update_packages(self):
        if self._update:
            self.installer.update_virtual_environments_packages()

    def clean_logs(self):
        logging.info("Running logs cleanup")
        today = datetime.today().date()
        threshold = today - timedelta(days=3)
        log_dir = self.root_dir / ".logs"
        if not log_dir.exists():
            return
        for log_date_dir in log_dir.iterdir():
            try:
                date = datetime.strptime(log_date_dir.name, "%Y_%m_%d").date()
            except ValueError:  # Skip folders that don't match the date format
                continue
            if date < threshold:
                logging.info(f"Removing logs : {log_date_dir}")
                shutil.rmtree(log_date_dir)

    def clean_jobs(self):
        logging.info("Running jobs cleanup")
        today = datetime.today().date()
        threshold = today - timedelta(days=3)
        job_dir = self.root_dir / ".jobs"
        if not job_dir.exists():
            return
        for job_date_dir in job_dir.iterdir():
            try:
                date = datetime.strptime(job_date_dir.name, "%Y_%m_%d").date()
            except ValueError:  # Skip folders that don't match the date format
                continue
            if date < threshold:
                logging.info(f"Removing jobs : {job_date_dir}")
                shutil.rmtree(job_date_dir)

    def clean_temp(self):
        logging.info("Running temp files cleanup")
        today = datetime.today().date()
        threshold = today - timedelta(days=3)
        job_dir = self.root_dir / ".temp"
        if not job_dir.exists():
            return
        for job_date_dir in job_dir.iterdir():
            try:
                date = datetime.strptime(job_date_dir.name, "%Y_%m_%d").date()
            except ValueError:  # Skip folders that don't match the date format
                continue
            if date < threshold:
                logging.info(f"Removing temp files : {job_date_dir}")
                shutil.rmtree(job_date_dir)

    def raise_error(self):
        """Only for debugging purposes"""
        import time

        time.sleep(5)
        raise RuntimeError("Something bad happened")

    def run_tasks(self):
        tasks: list[tuple[str, Callable]] = []
        tasks.append(("Toggle console...", self.toggle_console))
        tasks.append(("Connect to MongoDB server...", self.connect_to_mongodb_server))
        if self._update:
            tasks.append(("Fetching latest version...", self.fetch_version))
            tasks.append(("Updating virtual environments...", self.update_venvs))
            tasks.append(("Updating python packages...", self.update_packages))
        tasks.append(("Cleaning logs...", self.clean_logs))
        tasks.append(("Cleaning jobs...", self.clean_jobs))
        tasks.append(("Cleaning jobs...", self.clean_temp))
        # tasks.append(("Doing something risky", self.raise_error))  # For debugging purposes

        def run_next(i: int = 0):
            if i < len(tasks):
                message, func = tasks[i]
                self.set_status(message)
                QTimer.singleShot(100, lambda: self._execute(func, lambda: run_next(i + 1)))
            else:
                app = QApplication.instance()
                app.quit()

        run_next()

    def _execute(self, func, callback):
        # Run blocking func but keep repaint smooth
        QTimer.singleShot(10, lambda: self._blocking_call(func, callback))

    def _blocking_call(self, func: Callable, callback: Callable):
        try:
            func()
        except Exception as e:
            logging.error("Task failed", exc_info=True)
            self.set_status(f"Error: {e}")
            raise

        callback()


if __name__ == "__main__":
    show_splash_screen(update=False)
