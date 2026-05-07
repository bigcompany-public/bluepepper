from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TicketModel:
    name: str
    user: str
    computer: str
    description: str
    error: str = ""
    traceback: str = ""
    path: Path | None = None
    asset: str = ""
    shot: str = ""
    screenshots: list[Path] = field(default_factory=list[Path])
