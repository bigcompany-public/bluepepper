"""
Entry point of the main BluePepper application
Shows a splash screen to perform cleanup tasks and update BluePepper to the latest production version, and open BluePepper's
main window in a new process if everything went fine.
"""

import argparse
import os
import subprocess
from pathlib import Path

from bluepepper.app.splash_screen import show_splash_screen


def main(update: bool = False):
    success = show_splash_screen(update)
    if not success:
        return

    # Run she main window in a separate splash screen
    # As the update may have messed up a few packages, it is safer
    # to start with a brand new python environment
    root_dir = Path(os.environ["BLUEPEPPER_ROOT"])
    uv_path = root_dir / "bin/uv/uv.exe"
    command = [uv_path.as_posix(), "run"]

    # Run in the virtual environment defined by the "VIRTUAL_ENV" environment variable
    command += ["--active"]

    # Run the main event loop of the qt app
    script = root_dir / "bluepepper/app/main_window/main_window.py"
    command += [script.as_posix()]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update", action="store_true")
    args = parser.parse_args()
    main(args.update)
