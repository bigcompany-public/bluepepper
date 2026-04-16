import os
import uuid
from datetime import datetime
from pathlib import Path


def get_temp_path(app: str) -> Path:
    """
    Return path to a temp file, that contains the date and a unique id
    """
    root_path = Path(os.environ["BLUEPEPPER_ROOT"])
    now = datetime.now()
    day_str = now.strftime("%Y_%m_%d")
    now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    id = uuid.uuid4().hex
    return root_path / f".temp/{day_str}/{app}/{now_str}_{id}.temp"


if __name__ == "__main__":
    print(get_temp_path("demo"))
