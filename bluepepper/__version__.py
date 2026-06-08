from pathlib import Path

import toml

pyproject_path = Path(__file__).parent.parent.joinpath("pyproject.toml")
pyproject = toml.loads(pyproject_path.read_text())

__version__ = pyproject["project"]["version"]
