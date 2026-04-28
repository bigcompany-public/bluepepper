import json
import os
from pathlib import Path

from bluepepper.helpers.run_callable import run_function
from bluepepper.helpers.run_script import run_script


def main():
    mode = os.environ["BLUEPEPPER_BATCHER_MODE"]
    if mode == "script":
        run_batcher_script()
    else:
        run_batcher_function()


def run_batcher_script():
    run_script(
        path=Path(os.environ["BLUEPEPPER_BATCHER_SCRIPT"]), args=json.loads(os.environ["BLUEPEPPER_BATCHER_ARGS"])
    )


def run_batcher_function():
    run_function(
        module=os.environ["BLUEPEPPER_BATCHER_MODULE"],
        function=os.environ["BLUEPEPPER_BATCHER_FUNCTION"],
        kwargs=json.loads(os.environ["BLUEPEPPER_BATCHER_KWARGS"]),
    )


if __name__ == "__main__":
    main()
