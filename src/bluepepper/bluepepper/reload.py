import importlib
import logging
import os
import sys
from pathlib import Path


def reload_bluepepper_modules() -> None:
    """Reload all bluepepper modules.

    This function reloads all currently imported bluepepper modules, useful for
    development when module code changes without restarting the application.

    Usage:
        >>> from bluepepper import reload_bluepepper_modules
        >>> reload_bluepepper_modules()
    """
    bluepepper_package_path = Path(os.environ["BLUEPEPPER_ROOT"]) / "bluepepper"
    bluepepper_package_posix = bluepepper_package_path.as_posix()

    for module_name, module in list(sys.modules.items()):
        # Skip modules without file paths (built-ins, some packages like pywin32)
        module_file = getattr(module, "__file__", None)
        if not module_file:
            continue

        # Only reload modules from the bluepepper package
        if not Path(module_file).as_posix().startswith(bluepepper_package_posix):
            continue

        try:
            logging.debug(f"Reloading {module_name}")
            importlib.reload(module)
        except Exception as err:
            logging.warning(f"Failed to reload {module_name} ({err.__class__.__name__}: {err})")


if __name__ == "__main__":
    from bluepepper import __version__

    __version__.__version__ = "Changed version"
    print(__version__.__version__)

    reload_bluepepper_modules()
    print(__version__.__version__)
