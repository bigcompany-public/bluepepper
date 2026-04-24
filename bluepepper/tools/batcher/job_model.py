from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import List


class JobStatus(Enum):
    WAITING = auto()
    SUSPENDED = auto()
    RUNNING = auto()
    TERMINATED = auto()
    FINISHED = auto()
    ERROR = auto()


# Human-readable labels & colours for each status
STATUS_LABEL: dict[JobStatus, str] = {
    JobStatus.WAITING: "Waiting",
    JobStatus.SUSPENDED: "Not started",
    JobStatus.RUNNING: "Running",
    JobStatus.TERMINATED: "Terminated",
    JobStatus.FINISHED: "Finished",
    JobStatus.ERROR: "Error",
}

STATUS_COLOR: dict[JobStatus, str] = {
    JobStatus.WAITING: "#E0A030",
    JobStatus.SUSPENDED: "#888888",
    JobStatus.RUNNING: "#4A9EE0",
    JobStatus.TERMINATED: "#CC6633",
    JobStatus.FINISHED: "#4CAF50",
    JobStatus.ERROR: "#E05050",
}


@dataclass
class JobData:
    name: str
    description: str
    script_path: Path
    args: List[str] = field(default_factory=list[str])
    priority: int = 50
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    status: JobStatus = JobStatus.WAITING
    progress: int = 0
    notify_when_done: bool = False
