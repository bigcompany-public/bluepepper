from __future__ import annotations

import subprocess
import sys
import json
from io import StringIO
from typing import TYPE_CHECKING

from qtpy.QtCore import QThread, Signal
from pathlib import Path
import os

if TYPE_CHECKING:
    from bluepepper.tools.batcher.job_widget import JobWidget


class JobThread(QThread):
    """
    This class represents a QThread used by a big
    """

    _finished = Signal()
    _error = Signal()
    _progress = Signal(int)
    _log = Signal(str)
    _terminate = Signal()

    def __init__(self, job_widget: JobWidget):
        self.job_widget = job_widget
        self.job_data = job_widget.job_data
        super().__init__(job_widget)
        self.setup_signals()

    def setup_signals(self):
        self._log.connect(self.job_widget.update_log)
        self._progress.connect(self.job_widget.progress_bar.update_progress)
        self._finished.connect(self.job_widget.job_finished)
        self._error.connect(self.job_widget.error_encountered)
        self._terminate.connect(self.job_widget.terminate_job_from_script)

    @property
    def wrapper_script(self) -> Path:
        """Returns the path to the script that acts as a wrapper for the provided script/function"""
        return Path(__file__).with_name("batcher_wrapper.py")

    @property
    def script_env(self) -> dict[str, str]:
        env = os.environ.copy()
        mode = "module" if self.job_data.module else "script"
        env["BLUEPEPPER_BATCHER_MODE"] = mode
        env["BLUEPEPPER_BATCHER_SCRIPT"] = self.job_data.script_path.as_posix() if mode == "script" else ""
        env["BLUEPEPPER_BATCHER_ARGS"] = json.dumps(self.job_data.script_args) if mode == "script" else ""
        env["BLUEPEPPER_BATCHER_MODULE"] = self.job_data.module if mode == "module" else ""
        env["BLUEPEPPER_BATCHER_FUNCTION"] = self.job_data.func if mode == "module" else ""
        env["BLUEPEPPER_BATCHER_KWARGS"] = json.dumps(self.job_data.kwargs) if mode == "module" else ""
        return env

    def run(self):
        self._log.emit(f"Starting job {self.job_widget.job_data.name}")
        process = subprocess.Popen(
            [sys.executable, "-u", self.wrapper_script.as_posix()],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=self.script_env
        )

        stdout: StringIO = process.stdout  # type: ignore
        for line in stdout:
            line = line.rstrip()
            # Send all lines to the stdout label
            self._log.emit(line)

            # Emit progress to update the progress bar
            if "BLUEPEPPER_BATCHER_PROGRESS" in line:
                self._progress.emit(int(line.split("=")[-1].strip()))

            # This log line can be used to avoid stalling
            if "BLUEPEPPER_BATCHER_TERMINATE" in line:
                self._terminate.emit()
                return

        stdout.close()
        returncode = process.wait()

        if returncode != 0:
            self._error.emit()
            return

        self._finished.emit()
