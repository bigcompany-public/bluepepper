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
    args_str = os.environ["BLUEPEPPER_BATCHER_ARGS"]
    args_list = json.loads(args_str)
    formatted_args_list = []
    for arg in args_list:
        if isinstance(arg, str):
            formatted_args_list.append(arg)
        else:
            formatted_args_list.append(json.dumps(arg))

    run_script(path=Path(os.environ["BLUEPEPPER_BATCHER_SCRIPT"]), args=formatted_args_list)


def run_batcher_function():
    try:
        run_function(
            module=os.environ["BLUEPEPPER_BATCHER_MODULE"],
            function=os.environ["BLUEPEPPER_BATCHER_FUNCTION"],
            kwargs=json.loads(os.environ["BLUEPEPPER_BATCHER_KWARGS"]),
        )
    except Exception as err:
        print(f"BLUEPEPPER_BATCHER_ERROR={err}")
        raise


if __name__ == "__main__":
    main()
