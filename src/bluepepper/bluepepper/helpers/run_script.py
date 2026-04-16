
from pathlib import Path
import sys
import runpy


def run_script(path: Path, args=None):
    """
    This function runs the provided script with the provided arguments, and properly raises an
    error in case of failure
    """
    old_argv = sys.argv.copy()
    try:
        sys.argv = [str(path)] + (args or [])
        runpy.run_path(str(path), run_name="__main__")
    except SystemExit as e:
        raise RuntimeError(f"Script {path} exited with code {e.code}") from e
    finally:
        sys.argv = old_argv


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError("Please provide the path to the script to execute")
    path = Path(sys.argv[1])

    if len(sys.argv) > 2:
        run_script(path, sys.argv[2:])
    else:
        run_script(path)
