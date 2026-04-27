from __future__ import annotations

import subprocess
import sys
from io import StringIO
from typing import TYPE_CHECKING

from qtpy.QtCore import QThread, Signal

if TYPE_CHECKING:
    from bluepepper.tools.batcher.job_widget import JobWidget


class JobThread(QThread):
    """
    This class represents a QThread used by a big
    """

    finished = Signal()
    error = Signal()
    progress = Signal(int)
    log = Signal(str)

    def __init__(self, job_widget: JobWidget):
        self.job_widget = job_widget
        super().__init__(job_widget)
        self.setup_signals()

    def setup_signals(self):
        self.log.connect(self.job_widget.update_log)
        self.progress.connect(self.job_widget.progress_bar.update_progress)
        # self.finished.connect(self.job_widget.job_finished)
        self.error.connect(self.job_widget.error_encountered)

    def run(self):
        self.log.emit(f"Starting job {self.job_widget.job_data.name}")
        process = subprocess.Popen(
            [sys.executable, "-u", self.job_widget.job_data.script_path.as_posix()],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        stdout: StringIO = process.stdout  # type: ignore
        try:
            for line in stdout:
                line = line.rstrip()
                # Send all lines to the stdout label
                self.log.emit(line)

                # Emit progress to update the progress bar
                if "BLUEPEPPER_BATCHER_PROGRESS" in line:
                    self.progress.emit(int(line.split("=")[-1].strip()))

                # Fai
                if "BLUEPEPPER_BATCHER_TERMINATE" in line:
                    process.terminate()
                    self.error.emit()
                    break

        finally:
            stdout.close()
            returncode = process.wait()

        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, process.args)
        print("DONE")
