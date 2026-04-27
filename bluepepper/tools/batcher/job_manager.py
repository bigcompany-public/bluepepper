from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import QObject, QTimer, Slot

from bluepepper.tools.batcher.job_model import JobStatus

if TYPE_CHECKING:
    from bluepepper.tools.batcher.batcher_widget import BatcherWidget
    from bluepepper.tools.batcher.job_widget import JobWidget


class JobManager(QObject):
    """
    Orchestrates job scheduling.

    - Ticks every 500 ms.
    - On each tick, if auto-start is enabled and a thread slot is free,
      picks the highest-priority WAITING job (FIFO on ties) and emits
      ``should_start_job``.
    - Keeps a registry of JobData so priorities / statuses are tracked
      independently of the widgets.
    """

    def __init__(self, batcher: BatcherWidget) -> None:
        super().__init__(batcher)
        self.batcher = batcher

        # Configure timer
        self._timer = QTimer(self)
        self._timer.setInterval(500)
        self._timer.timeout.connect(self._tick)

    def start_event_loop(self):
        self._timer.start()

    @Slot()
    def _tick(self) -> None:
        if not self.auto_start:
            return

        # Stop if no jobs
        widgets = self.batcher.job_widgets
        if not widgets:
            return

        # Stop if the current running jobs exceed the max thread limit
        running_jobs_count = len([widget for widget in widgets if widget.job_data.status == JobStatus.RUNNING])
        if running_jobs_count >= self.max_threads:
            return

        # Get jobs to start
        sorted_widgets = sorted(
            widgets,
            key=lambda job_widget: (-job_widget.job_data.priority, job_widget.job_data.created_at),
        )

        jobs_to_start: list[JobWidget] = []
        for widget in sorted_widgets:
            # Only keep waiting job (ignore terminated, error, suspended...)
            if widget.job_data.status != JobStatus.WAITING:
                continue

            jobs_to_start.append(widget)
            # Limit number of jobs to start to max threads
            if len(jobs_to_start) + running_jobs_count >= self.max_threads:
                break

        # Emit start signals
        for job in jobs_to_start:
            job.start()

    @property
    def max_threads(self) -> int:
        return self.batcher.spinbox_max_threads.value()

    @property
    def auto_start(self) -> bool:
        return self.batcher.cb_auto_start.isChecked()

    @property
    def delete_finished(self) -> bool:
        return self.batcher.cb_delete_finished.isChecked()
