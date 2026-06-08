#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the open_file function,
used to standardize the way files are opened
"""

import argparse
import json
import logging
import os
import subprocess
import webbrowser
from pathlib import Path

from bluepepper.core import root_dir
from bluepepper.helpers.run_callable import run_callable

OPENFILE_CONFIG_FILE = root_dir / "conf/openfile.json"
OPENFILE_CONFIG: dict = json.loads(OPENFILE_CONFIG_FILE.read_text())


def open_file(path: Path, os_default=False):
    """
    This function is used to standardize the way files are opened
    based on their file extension

    :param path: Path of the file to open
    :type path: Path
    """
    path = Path(path)

    # Cover the case of urls
    if str(path).startswith("http"):
        webbrowser.open(path.as_posix())
        return

    # Return if the provided file does not exist
    if not path.exists():
        logging.error("Path does not exist : %s", path)
        return

    # Open with windows default software
    if os_default:
        os.startfile(path)
        return

    # Reveal in explorer if the provided path is a folder
    if path.is_dir():
        os.startfile(path)
        return

    # Get specific extension management
    extension_config: dict = OPENFILE_CONFIG.get(path.suffix, {})
    if extension_config:
        _kwargs = {}
        kwargs: dict[str, str] = extension_config.get("kwargs", {})
        for key, value in kwargs.items():
            _kwargs[key] = value
            if value == "<path>":
                _kwargs[key] = path.as_posix()

        run_callable(extension_config["module"], extension_config["function"], kwargs=_kwargs)
        return

    # Open with windows default
    os.startfile(path)


def show_in_explorer(path: Path):
    path = Path(path)
    # Notes :
    # - doesn't work with forward slashes
    # - doesn't work with commands provided as a list if the path contains spaces (a string with quotes is used instead)
    subprocess.Popen(f'explorer.exe /select,"{path}"')


def read_as_vlc_playlist(paths: list[Path]):
    vlc = Path(r"C:\Program Files\VideoLAN\VLC\vlc.exe").as_posix()
    paths = [str(Path(path)) for path in paths]
    command = [vlc] + paths
    subprocess.Popen(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True, type=str)
    args = parser.parse_args()
    open_file(args.path)
