"""
There is two main ways of opening maya : in interactive mode (the normal way, with an interface)
and in batch mode (on the renderfarm for instance)
- In interactive mode, the initialization of bluepepper must be called within the utils.executeDeferred
function, and display a warning on error
- In batch mode, the main function can be called directly, and should close maya with a return code
that indicates an error has occured
"""

import json
import logging
import os
import shutil
import traceback
from pathlib import Path
from typing import Optional

from maya import cmds, utils
from maya.api import OpenMaya

_LAST_KNOWN_PATH: Optional[Path] = None
_IMPORT_ERROR = None
try:
    # WARNING :
    # userSetup.py uses utils.executeDeferred() for deferred initialization, which means
    # import errors won't be displayed in the console if they occur during the deferred
    # execution. Import errors are most likely due to an issue with maya's UV virtual environment
    from bluepepper.core import init_logging, root_dir, user_prefs_dir
    from bluepepper.helpers.run_callable import run_function
    from bluepepper.helpers.run_script import run_script
except Exception:
    _IMPORT_ERROR = traceback.format_exc()


def main():
    if _IMPORT_ERROR:
        # Use print instead of logging, in case the logger failed to initialize
        print("################################")
        print("# BLUEPEPPER INITIALIZATION ERROR #")
        print("################################")
        print(_IMPORT_ERROR)
        cmds.inViewMessage(
            amg="⚠️ An error was encourtered while loading bluepepper modules. See logs for more details",
            pos="topCenter",
            fade=False,
        )
        return

    if cmds.about(batch=True):
        batch_mode_initialization()
    else:
        utils.executeDeferred(gui_mode_initialization)


def gui_mode_initialization():
    """
    Runs initialization in a try-except block, and displays a message on error without closing maya
    """
    init_logging("maya")
    try:
        initialize()
    except:
        logging.error("################################")
        logging.error("# BLUEPEPPER INITIALIZATION ERROR #")
        logging.error("################################")
        cmds.inViewMessage(
            amg="⚠️ An error was encourtered while initializing bluepepper. See logs for more details",
            pos="topCenter",
            fade=False,
        )
        logging.error(traceback.format_exc())


def batch_mode_initialization():
    """
    Runs initialization in a try-except block, and closes maya on error
    """
    try:
        initialize()
    except:
        logging.error("################################")
        logging.error("# BLUEPEPPER INITIALIZATION ERROR #")
        logging.error("################################")
        logging.error(traceback.format_exc())
        os._exit(1)


def initialize():
    """This function is run at the startup of maya"""
    logging.info("Running BluePepper's userSetup.py")

    set_workspace()
    setup_callbacks()
    open_startup_scene()
    run_startup_script()
    run_startup_function()
    # configure_plugins()
    logging.info("BluePepper was successfully initialized")


def set_workspace(path: Path = None):
    """
    Sets the workspace to the directory "workspace" right next to the maya file
    A dedicated "workspace" folder is used, because the working directory can turn into a mess
    when a bunch of subfolders are created
    """
    # Get workspace dir to use based on the scene path
    path = path or cmds.file(q=True, sn=True)
    if not path:
        workspace_dir = user_prefs_dir / "maya/temp/workspace"
    else:
        workspace_dir = Path(path).parent / "workspace"

    # Copy workspace.mel file if needed
    workspace_mel_src = root_dir / "conf/maya/workspace.mel"
    workspace_mel_dst = workspace_dir / "workspace.mel"
    if not workspace_mel_dst.exists():
        workspace_mel_dst.parent.mkdir(exist_ok=True, parents=True)
        logging.info(f"Copying {workspace_mel_src} to {workspace_mel_dst}")
        shutil.copy(workspace_mel_src, workspace_mel_dst)

    # Set workspace
    logging.info(f"Setting workspace to {workspace_dir}")
    cmds.workspace(workspace_dir.as_posix(), openWorkspace=True)


def open_startup_scene():
    """
    This function opens the scene specified by the BIG_STARTUP_SCENE environment variable
    """
    path = os.environ["BLUEPEPPER_STARTUP_SCENE"]
    if not path:
        return
    path = Path(path)

    ref_mode = os.environ.get("BLUEPEPPER_REFERENCE_MODE", "last")
    if ref_mode == "last":
        logging.info(f"Opening file {path}")
        cmds.file(path.as_posix(), o=True, f=True)

    elif ref_mode == "none":
        logging.info(f"Opening file without loading references : {path}")
        cmds.file(path.as_posix(), o=True, f=True, loadReferenceDepth="none")

    elif ref_mode == "all":
        logging.info(f"Opening file with all references : {path}")
        cmds.file(path.as_posix(), o=True, f=True, loadReferenceDepth="all")

    elif ref_mode == "select":
        reference_nodes = os.environ["BIG_REFERENCE_NODES_TO_LOAD"]
        logging.info(f"Opening file with selective preload : {path} : {reference_nodes}")
        reference_nodes: list[str] = json.loads(reference_nodes)
        cmds.file(path.as_posix(), o=True, f=True, loadReferenceDepth="none")
        for reference_node in reference_nodes:
            cmds.file(loadReference=reference_node, loadReferenceDepth="topOnly")

    # Fix ctrl+s sometimes not working
    cmds.file(rename=path.as_posix())


def setup_callbacks():
    """Sets up various callbacks"""
    logging.info("Setup callbacks file Open/Save callbacks")
    callback = OpenMaya.MSceneMessage.kAfterSave
    OpenMaya.MSceneMessage.addCallback(callback, after_save_callback)

    callback = OpenMaya.MSceneMessage.kAfterOpen
    OpenMaya.MSceneMessage.addCallback(callback, after_open_callback)

    callback = OpenMaya.MSceneMessage.kAfterNew
    OpenMaya.MSceneMessage.addCallback(callback, after_new_callback)


def after_open_callback(path):
    store_scene_path(path)
    set_workspace(path)


def after_new_callback(path):
    store_scene_path(path)
    set_workspace(path)


def after_save_callback(path):
    store_scene_path(path)


def store_scene_path(path):
    global _LAST_KNOWN_PATH
    _path = cmds.file(q=True, sn=True) or None
    logging.info(f"Storing last known scene : {_path}")
    if not _path:
        _LAST_KNOWN_PATH = None
        return
    _LAST_KNOWN_PATH = Path(_path)


def run_startup_script():
    """
    This function runs the script specified by the BLUEPEPPER_STARTUP_SCRIPT environment variable
    """
    path = os.environ.get("BLUEPEPPER_STARTUP_SCRIPT")
    if not path:
        return
    path = Path(path)
    logging.info(f"Running startup script : {path}")
    run_script(path)


def run_startup_function():
    """
    This function runs the function specified by a set on environment variables
    """
    module = os.environ.get("BLUEPEPPER_STARTUP_MODULE")
    if not module:
        return

    func = os.environ.get("BLUEPEPPER_STARTUP_FUNCTION")
    # Expected to be provided as a string representing a dict
    kwargs = os.environ.get("BLUEPEPPER_STARTUP_KWARGS")
    kwargs = json.loads(kwargs) if kwargs else None
    run_function(module, func, kwargs=kwargs)


if __name__ == "__main__":
    main()
