#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the BlenderLauncher class, used to open blender in a standardized way
"""

import argparse
import os
import subprocess
from pathlib import Path
from typing import Optional

from conf.blender import BlenderConfig

from bluepepper.core import root_dir
from bluepepper.logger import get_log_path


class BlenderLauncher:
    """
    This class is designed to open Blender in a standardized way,
    mostly by settings environment variables
        - PYTHONPATH is used to import modules from bluepepper, and from blender's virtual environment

    It also contains methods to ensure and reset preferences
    """

    def __init__(
        self,
        path: Path | None = None,
        script: Path | None = None,
        app_template: str | None = None,
    ):
        """
        Constructor method
        """
        self.startup_scene = Path(path) if path else None
        self.startup_script = Path(script) if script else None
        self.app_template = app_template

    def get_executable(self) -> Path:
        """Returns the path to blender.exe"""
        for path in BlenderConfig.executable_paths:
            if path.exists():
                return path
        raise Exception("No blender installation was found on this computer")

    @property
    def env(self) -> dict[str, str]:
        """
        Returns the environment variables to use within blender
        :return: Environment variables
        :rtype: dict
        """
        # Get environment variables (including the ones defined in bluepepper.py)
        env = os.environ.copy()

        # Append blender-specific environment variables
        env.update(BlenderConfig.env)

        # Set PYTHONPATH used by blender to import site packages
        env["PYTHONPATH"] = ";".join([str(path) for path in self.pythonpaths])
        # BLENDER_USER_SCRIPTS must be set, not BLENDER_SYSTEM_SCRIPTS
        env["BLENDER_USER_SCRIPTS"] = self.script_dir.as_posix()
        return env

    @property
    def venv_site_package_path(self) -> Path:
        """
        Returns the paths to the packages intalled in a python virtual environment setup with UV,
        that matches the python version of maya
        """
        venv_dir = root_dir / "venvs" / BlenderConfig.venv
        site_package_dir = venv_dir / "Lib/site-packages"
        return site_package_dir

    @property
    def pythonpaths(self) -> list[Path]:
        """
        Returns the PYTHONPATH string used as an environment variable
        """
        return [
            # Add pipeline root to python path, in order to import bluepepper modules
            root_dir,
            # add virtual environment to python path, in order to import packages installed with uv
            self.venv_site_package_path,
        ]

    @property
    def script_dir(self) -> Path:
        """Directory where addons shoul be placed"""
        return root_dir / "blender" / "blender_scripts_dir"

    def open(self):
        """This method opens blender"""
        command = [self.get_executable().as_posix()]

        # App template
        if self.app_template:
            command += ["--app-template", self.app_template]

        # Startup scene
        if self.startup_scene:
            command += [self.startup_scene.as_posix()]
        # command += [
        #     "--addons",
        #     "bluepepper_addon",  # Addon must be called by the name of the module
        # ]

        # Startup script
        command += [
            "--python",
            self.startup_wrapper.as_posix(),
            "--python-exit-code",  # Force blender to have a return code of 1 in case of error
            "1",
        ]

        # Since blender 5.0, a specific options has to be added in order to effectively use PYTHONPATH
        command.append("--python-use-system-env")

        # Log file
        log_path = get_log_path("blender")
        env = self.env.copy()
        env["BLUEPEPPER_LOG_PATH"] = log_path.as_posix()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        command += ["--log-file", log_path.as_posix()]
        self.process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )

    @property
    def startup_wrapper(self) -> Path:
        """Returns the path to the script that runs when blender starts"""
        return root_dir / "bluepepper/softwares/blender/startup.py"


def open(path: Optional[Path] = None, script: Optional[Path] = None):
    maya = BlenderLauncher(path=path, script=script)
    maya.open()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=False, help="Path to the blend file to open")
    parser.add_argument("-s", "--script", required=False, help="Path to the blend file to open")
    parser.add_argument("-a", "--app_template", required=False, help="Name of the app template")
    args = parser.parse_args()

    app = BlenderLauncher(path=args.path, script=args.script, app_template=args.app_template)
    app.open()
