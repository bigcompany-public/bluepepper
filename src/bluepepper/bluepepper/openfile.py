#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the open_file function,
used to standardize the way files are opened
"""

import os
import logging
import webbrowser
import argparse
import subprocess
from typing import List
from pathlib import Path


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
        webbrowser.open(path)
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
        webbrowser.open(path)
        return

    # Get extension & software assigned to it
    if path.suffix in [".ma", ".mb"]:
        print("Open in maya")
    elif path.suffix == ".blend":
        print("Open in photoshop")
    elif path.suffix in [".mov", ".mp4"]:
        print("Open in vlc")
    elif path.suffix == ".nk":
        print("Open in nuke")


def show_in_explorer(path: Path):
    path = Path(path)
    subprocess.Popen(["explorer.exe", f'/select,{path}'])


def read_as_vlc_playlist(paths: List[Path]):
    vlc = Path(r"C:\Program Files\VideoLAN\VLC\vlc.exe").as_posix()
    paths = [str(Path(path)) for path in paths]
    command = [vlc] + paths
    subprocess.Popen(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True, type=str)
    args = parser.parse_args()
    open_file(args.path)
