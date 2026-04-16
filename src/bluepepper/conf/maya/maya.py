from pathlib import Path


class MayaConfig:
    executable_paths = [Path(r"C:\Program Files\Autodesk\Maya2025\bin\maya.exe")]
    env: dict[str, str] = {}
    venv: str = "maya_3.11.4"
