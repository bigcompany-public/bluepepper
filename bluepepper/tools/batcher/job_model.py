from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum, auto
from pathlib import Path
from typing import List


class JobStatus(StrEnum):
    WAITING = auto()
    RUNNING = auto()
    FINISHED = auto()
    SUSPENDED = auto()
    TERMINATED = auto()
    ERROR = auto()


@dataclass
class JobData:
    name: str
    description: str
    script_path: Path = field(default=Path())
    script_args: List[str] = field(default_factory=list[str])
    module: str = ""
    func: str = ""
    kwargs: dict = field(default_factory=dict)
    priority: int = 50
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    created_at: datetime = field(default_factory=datetime.now, init=False)
    status: JobStatus = field(default=JobStatus.WAITING, init=False)
    progress: int = field(default=0, init=False)
    notify_when_done: bool = False
