from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectSettings:
    project_name: str = "projectName"
    project_code: str = "code"
    width: int = 1920
    height: int = 1080
    fps: float = 25.0
    start_frame: int = 101
    production_trackers: list[str] = ["aquarium"]
