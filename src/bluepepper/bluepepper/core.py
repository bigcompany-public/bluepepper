import os
from pathlib import Path

from conf.lucent_config import codex

from bluepepper.__version__ import __version__ as version
from bluepepper.database import database
from bluepepper.logger import init_logging
from bluepepper.reload import reload_bluepepper_modules
from bluepepper.temp import get_temp_path

if not os.environ.get("BLUEPEPPER_ROOT"):
    raise RuntimeError(
        'The environment variable "BLUEPEPPER_ROOT" was not found. Please make sure to initialize bluepepper'
    )

root_dir = Path(os.environ["BLUEPEPPER_ROOT"])
user_prefs_dir = root_dir.parent / f"{root_dir.name}_userprefs/{os.environ['USERNAME']}"

__all__ = [
    "codex",
    "database",
    "init_logging",
    "get_temp_path",
    "version",
    "reload_bluepepper_modules",
    "root_dir",
    "user_prefs_dir",
]
