#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the BlenderLauncher class, used to open blender in a standardized way
"""

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from bluepepper.core import root_dir
from bluepepper.logger import get_log_path
from conf.blender import BlenderConfig


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
        that matches the python version of blender
        """
        venv_dir = root_dir / "venvs" / BlenderConfig.venv
        site_package_dir = venv_dir / "Lib/site-packages"
        return site_package_dir

    @property
    def pythonpaths(self) -> list[Path]:
        """
        Returns the PYTHONPATH string used as an environment variable
        """
        paths = [
            # Add pipeline root to python path, in order to import bluepepper modules
            root_dir,
            # add virtual environment to python path, in order to import packages installed with uv
            self.venv_site_package_path,
        ]

        # Add editable mode packages (dev only)
        from urllib.parse import urlparse
        from urllib.request import url2pathname

        # p = urlparse('file:///home/pi/Desktop/music/Radio%20Song.mp3')
        # file_path = url2pathname(p.path)
        for i in self.venv_site_package_path.rglob("direct_url.json"):
            url = json.loads(i.read_text())["url"]
            path = Path(url2pathname(urlparse(url).path))
            paths.append(path / "src")

        return paths

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
            command += [str(self.startup_scene)]
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

        # Open Blender with a separate console and hide console by default
        # This must be done so blender doesn't use bluepepper's console and so "toggle system console" works as intended
        flag = subprocess.CREATE_NEW_CONSOLE
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        self.process = subprocess.Popen(
            command,
            env=env,
            creationflags=flag,
            startupinfo=startupinfo,
        )

    @property
    def startup_wrapper(self) -> Path:
        """Returns the path to the script that runs when blender starts"""
        return root_dir / "bluepepper/softwares/blender/startup.py"


def open(path: Optional[Path] = None, script: Optional[Path] = None):
    print(path)
    blender = BlenderLauncher(path=path, script=script)
    blender.open()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=False, help="Path to the blend file to open")
    parser.add_argument("-s", "--script", required=False, help="Path to the blend file to open")
    parser.add_argument("-a", "--app_template", required=False, help="Name of the app template")
    args = parser.parse_args()

    app = BlenderLauncher(path=args.path, script=args.script, app_template=args.app_template)
    app.open()
