import logging
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Generator

import psutil
from bluepepper.core import get_temp_path, init_logging, root_dir
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self):
        self.screenshot_event = threading.Event()
        self.new_file_path = None

    def on_created(self, event):
        if not event.is_directory:
            self.new_file_path = event.src_path
            self.screenshot_event.set()


class EscWatcher:
    """
    Listens for ESC using pynput, sets event immediately.
    """

    def __init__(self):
        self.esc_event = threading.Event()
        self.listener = KeyboardListener(on_press=self._on_press)

    def _on_press(self, key: Key) -> bool | None:
        if key == Key.esc:
            self.esc_event.set()
            # Stop listener
            return False

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()


class GinkScreenshot:
    def __init__(self) -> None:
        self.executable = root_dir / "bin/gink/gInk.exe"
        self.config_file = self.executable.with_name("config.ini")
        self.destination_dir = get_temp_path("screenshotGink").parent
        self.current_destination_dir: Path = None
        self.keyboard = KeyboardController()
        self.gink_process: psutil.Process = None
        self.gink_needs_restart = False

    def capture_screenshot(self):
        self.get_gink_process()
        self.get_destination_dir()
        if self.current_destination_dir != self.destination_dir:
            self.kill_gink()
            self.set_destination_dir()
        self.create_destination_dir()
        self.start_gink()
        self.open_gink()
        return self.wait_for_new_screenshot()

    def get_gink_process(self) -> psutil.Process | None:
        processes: Generator[psutil.Process] = psutil.process_iter()
        for process in processes:
            if process.name() == self.executable.name:
                self.gink_process = process

    def get_destination_dir(self):
        content = self.config_file.read_text()
        _match = re.search(r"Snapshot_Path =(.+)", content)
        self.current_destination_dir = Path(_match.group(1).strip())

    def create_destination_dir(self):
        self.destination_dir.mkdir(parents=True, exist_ok=True)

    def kill_gink(self):
        if not self.gink_process:
            return
        logging.info("Killing Gink")
        self.gink_process.kill()
        self.gink_process = None

    def start_gink(self):
        if self.gink_process:
            return
        logging.info(f"Starting {self.executable.name}")
        subprocess.Popen([self.executable.as_posix()])
        time.sleep(1)

    def set_destination_dir(self):
        logging.info(f"Setting destination dir to {self.destination_dir}")
        with self.config_file.open("r") as file:
            lines = file.readlines()

        with self.config_file.open("w") as file:
            for line in lines:
                if line.strip().startswith("Snapshot_Path"):
                    file.write(f"Snapshot_Path = {self.destination_dir.as_posix()}\n")
                else:
                    file.write(line)

    def open_gink(self):
        """
        Replace pyautogui.hotkey('ctrl', 'alt', 'g') with pynput.
        """
        self.keyboard.press(Key.ctrl_l)
        self.keyboard.press(Key.alt_l)
        self.keyboard.press("g")

        self.keyboard.release("g")
        self.keyboard.release(Key.alt_l)
        self.keyboard.release(Key.ctrl_l)

    def wait_for_new_screenshot(self, timeout: int = 30):
        logging.info("Waiting for new screenshot...")

        # Create handler that looks for new files
        event_handler = ScreenshotHandler()
        observer = Observer()
        observer.schedule(
            event_handler, self.destination_dir.as_posix(), recursive=False
        )
        observer.start()

        # Create handler that checks if escape gets pressed
        esc_watcher = EscWatcher()
        esc_watcher.start()

        start_time = time.time()
        try:
            while True:
                # 1) Screenshot created
                if event_handler.screenshot_event.is_set():
                    new_path = Path(event_handler.new_file_path)
                    logging.info(f'Screenshot saved: "{new_path}"')
                    return new_path

                # 2) ESC pressed
                if esc_watcher.esc_event.is_set():
                    logging.info("ESC pressed — cancelling screenshot.")
                    return None

                # 3) Timeout
                if time.time() - start_time > timeout:
                    logging.warning("No screenshot detected — timeout.")
                    return None

                time.sleep(0.05)

        finally:
            observer.stop()
            observer.join()
            esc_watcher.stop()


def capture_screenshot() -> Path | None:
    gs = GinkScreenshot()
    return gs.capture_screenshot()


if __name__ == "__main__":
    init_logging("screenshot")
    gs = GinkScreenshot()
    gs.capture_screenshot()
