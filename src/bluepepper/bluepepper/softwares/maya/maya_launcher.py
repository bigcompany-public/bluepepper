import argparse
import ast
import json
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from conf.maya.maya import MayaConfig

from bluepepper.core import init_logging, root_dir, user_prefs_dir


class MayaLauncher:
    def __init__(
        self,
        path: Optional[Path] = None,
        script_path: Optional[Path] = None,
        reference_mode: Optional[str] = None,
        module: Optional[str] = None,
        func: Optional[str] = None,
        kwargs: Optional[dict] = None,
    ):
        self.path = Path(path) if path else self.default_scene_path
        self.script_path = Path(script_path) if script_path else None
        self.reference_mode = reference_mode
        self.module = module
        self.func = func
        self.kwargs = kwargs

    @property
    def default_scene_path(self) -> Path:
        return ""

    @property
    def executable(self) -> Path:
        for path in MayaConfig.executable_paths:
            if path.exists():
                return path
        raise FileNotFoundError("No maya executable found")

    @property
    def maya_app_dir(self) -> Path:
        """Returns the path to the preferences folder"""
        return user_prefs_dir / "maya/maya_app_dir"

    @property
    def default_maya_app_dir(self) -> Path:
        """
        Returns the path to the default preferences to copy to the user's maya_app directory,
        the first time the user launches maya
        """
        return root_dir / "conf/maya/default_maya_app_dir"

    @property
    def shelf_paths(self) -> list[Path]:
        """Returns the paths where maya should look for .mel shelves"""
        return [root_dir / "conf/maya/shelves"]

    @property
    def icons_paths(self) -> list[Path]:
        """Returns the paths where maya should look for scripts"""
        return [root_dir / "bluepepper/gui/icons"]

    @property
    def venv_site_package_path(self) -> Path:
        """
        Returns the paths to the packages intalled in a python virtual environment setup with UV,
        that matches the python version of maya
        """
        venv_dir = root_dir / "venvs" / MayaConfig.venv
        site_package_dir = venv_dir / "Lib/site-packages"
        return site_package_dir

    @property
    def python_paths(self) -> list[Path]:
        """Returns the paths from which python should be allowed to import modules"""
        return [
            # Add pipeline root to python path, in order to import bluepepper modules
            root_dir,
            # add virtual environment to python path, in order to import packages installed with uv
            self.venv_site_package_path,
            # Add path to userSetup.py responsible for the initialization of maya
            root_dir / "conf/maya/startup",
        ]

    @property
    def local_env(self) -> dict[str, str]:
        env = {}

        # Update maya-specific environement variables
        env["MAYA_APP_DIR"] = self.maya_app_dir.as_posix()
        env["MAYA_SHELF_PATH"] = ";".join([path.as_posix() for path in self.shelf_paths])
        env["MAYA_SCRIPT_PATH"] = (Path(__file__).parent / "startup").as_posix()
        env["XBMLANGPATH"] = ";".join([path.as_posix() for path in self.icons_paths])

        # Configure PYTHONPATH so bluepepper modules & other packages can be imported easily
        env["PYTHONPATH"] = ";".join([path.as_posix() for path in self.python_paths])

        # Set scene to open (opened through userSetup.py)
        # Startup scene is set this way to provide more control over how the scene is supposed to
        # open (namely the way references are handled)
        env["BLUEPEPPER_STARTUP_SCENE"] = self.path.as_posix() if self.path else ""
        env["BLUEPEPPER_REFERENCE_MODE"] = self.reference_mode if self.reference_mode else ""

        # Set script to run on startup logic (executed through userSetup.py)
        env["BLUEPEPPER_STARTUP_SCRIPT"] = self.script_path.as_posix() if self.script_path else ""
        env["BLUEPEPPER_STARTUP_MODULE"] = self.module if self.module else ""
        env["BLUEPEPPER_STARTUP_FUNCTION"] = self.func if self.func else ""
        env["BLUEPEPPER_STARTUP_KWARGS"] = json.dumps(self.kwargs) if self.kwargs else ""

        return env

    def open(self):
        self.ensure_preferences()
        # self.ensure_splash_screen()
        command = [self.executable.as_posix()]
        env = os.environ.copy()
        env.update(self.local_env)
        subprocess.Popen(command, env=env)

    def ensure_preferences(self):
        """Create a preference folder if it does not exist yet"""
        if self.maya_app_dir.exists():
            return

        logging.info(f"Cloning default preferences to {self.maya_app_dir}")
        shutil.copytree(self.default_maya_app_dir, self.maya_app_dir)

        # Userpref file must be fixed because it contains hard coded paths
        userpref_files = self.maya_app_dir.glob("*/prefs/userPrefs.mel")
        for userpref_file in userpref_files:
            content = userpref_file.read_text()

            pattern = r' -sva "SafeModeUserSetupHash" ".*?"\n'
            content = re.sub(pattern, "", content)

            # Project path
            pattern = r' -sv "lastLocalWS" ".*?"'
            new_path = self.maya_app_dir / "projects/default"
            new_string = f'-sv "lastLocalWS" "{new_path.as_posix()}"'
            content = re.sub(pattern, new_string, content)

            userpref_file.write_text(content)

    def remove_maya_app_dir(self):
        """Removes maya_app_dir in order to reset maya's preferences"""
        if self.maya_app_dir.exists():
            shutil.rmtree(self.maya_app_dir)


def open(
    path: Optional[Path] = None,
    script: Optional[Path] = None,
    module: Optional[str] = None,
    func: Optional[str] = None,
    kwargs: Optional[dict] = None,
    reference_mode: Optional[str] = "last",
):
    maya = MayaLauncher(
        path=path,
        script_path=script,
        reference_mode=reference_mode,
        module=module,
        func=func,
        kwargs=kwargs,
    )
    maya.open()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=False, help="Path to the maya scene to open")
    parser.add_argument(
        "-s",
        "--script",
        required=False,
        help="Path to the python startup script to execute",
    )
    parser.add_argument("-m", "--module", required=False, help="python module")
    parser.add_argument("-f", "--function", required=False, help="python function")
    parser.add_argument("-k", "--kwargs", required=False, help="keyword arguments for function")
    parser.add_argument("-rm", "--reference_mode", required=False, default="last")
    args = parser.parse_args()

    init_logging("maya")
    maya = MayaLauncher(
        path=args.path,
        reference_mode=args.reference_mode,
        script_path=args.script,
        module=args.module,
        func=args.function,
        kwargs=ast.literal_eval(args.kwargs) if args.kwargs else None,
    )
    maya.open()
