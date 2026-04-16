from pathlib import Path


class BlenderConfig:
    executable_paths = [Path(r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe")]
    env: dict[str, str] = {}
    venv: str = "blender_3.13.9"
