"""BluePepper installation and environment management system.

This module provides automated installation, virtual environment setup,
and repository management for the BluePepper project.
"""

import logging
import os
import shutil
import subprocess
import sys
import time
import traceback
from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, List, TypeVar
from urllib.request import urlopen


def _main(
    update_repository: bool = False,
    reset: bool = False,
    update_packages: bool = False,
) -> None:
    """Execute the BluePepper installation process.

    Args:
        update_repository: Whether to update the git repository to the current tag.
        reset: Whether to remove existing virtual environments before installation.
        update_packages: Whether to update packages in existing virtual environments.

    Raises:
        SystemExit: If installation fails, exits with code 1.
    """
    try:
        bluepepper = BluePepperInstaller(
            update_repository=update_repository,
            update_packages=update_packages,
            reset=reset,
        )
        bluepepper.install()
    except Exception:
        logging.error(traceback.format_exc())
        input("Press any key to continue...")
        sys.exit(1)


def timeit(func):
    """Decorator to measure and log function execution time.

    Args:
        func: The function to be timed.

    Returns:
        Wrapped function that logs its execution time.
    """

    @wraps(func)
    def timeit_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__} took {total_time:.4f} seconds")
        return result

    return timeit_wrapper  # type: ignore[return-value]


class BluePepperInstaller:
    """Manages BluePepper installation, virtual environments, and repository updates.

    This class handles the complete installation workflow including:
    - Git repository management and version control
    - Virtual environment creation and package installation
    - Desktop shortcut creation
    - Environment variable configuration

    Attributes:
        root_path: Root directory of the BluePepper installation.
        update_repository: Flag to update git repository to current tag.
        update_packages: Flag to update packages in virtual environments.
        reset: Flag to remove existing virtual environments.
    """

    def __init__(
        self,
        update_repository: bool = False,
        reset: bool = False,
        update_packages: bool = False,
    ) -> None:
        """Initialize the BluePepper installer.

        Args:
            update_repository: Whether to update the git repository.
            reset: Whether to reset (remove) existing virtual environments.
            update_packages: Whether to update packages in virtual environments.
        """
        self.root_path = Path(__file__).parent.parent

        # Configure environment variables
        os.environ["BLUEPEPPER_LOG_LEVEL"] = "INFO"
        os.environ["BLUEPEPPER_ROOT"] = self.root_path.as_posix()
        if not os.environ.get("BLUEPEPPER_SESSION_ID"):
            os.environ["BLUEPEPPER_SESSION_ID"] = "installer"

        # Enforce UV python directory to be user-independent
        os.environ["UV_PYTHON_INSTALL_DIR"] = (self.root_path / ".uv_python").as_posix()

        # Enforce the UV virtual environment for script execution
        os.environ["VIRTUAL_ENV"] = self.core_python_exe.parent.parent.as_posix()

        self.update_repository = update_repository
        self.update_packages = update_packages
        self.reset = reset

    @timeit
    def install(self) -> None:
        """Execute the complete installation workflow.

        This method orchestrates the installation process:
        1. Initializes logging
        2. Updates git repository if requested
        3. Resets virtual environments if requested
        4. Sets up virtual environments
        5. Updates packages if requested
        6. Creates desktop shortcuts
        """
        init_logging("installer")
        logging.info("Installing BluePepper")

        if self.update_repository:
            logging.info("Updating git repository")
            self.fetch_current_tag()

        if self.reset:
            logging.info("Resetting BluePepper installation")
            self.remove_virtual_environments()

        self.setup_virtual_environments()

        if self.update_packages:
            self.update_virtual_environments_packages()

        self.create_shortcuts()

    def fetch_current_tag(self) -> None:
        """Fetch and checkout the current git tag from the shared location.

        This method ensures all users run the same version by:
        1. Reading the current tag from a shared URL
        2. Fetching the latest repository state
        3. Checking out the specified tag

        Returns early if running from a network path or developer workspace.

        Raises:
            subprocess.CalledProcessError: If git commands fail.
        """
        if self.current_dir_is_network_path():
            logging.warning(
                "The installation script is running on a network path (most likely Gitlab CI/CD). Aborting..."
            )
            return

        # Retrieve current tag from server
        current_tag = self.current_tag

        # Add current directory to safe directories for multi-user access
        command = [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            self.root_path.as_posix(),
        ]
        subprocess.run(command, check=True, cwd=self.root_path)

        # Clear any changes to ensure clean repository state
        logging.info("Git - Fetching repository")
        subprocess.run(["git", "fetch", "origin"], check=True, cwd=self.root_path, text=True)

        branch = "main"
        logging.info(f"Git - Checkout to {branch}")
        subprocess.run(["git", "checkout", branch], check=True, cwd=self.root_path, text=True)
        subprocess.run(["git", "pull"], check=True, cwd=self.root_path, text=True)

        logging.info("Git - Reverting changes")
        subprocess.run(
            ["git", "reset", "--hard", "origin/main"],
            check=True,
            cwd=self.root_path,
            text=True,
        )
        subprocess.run(["git", "clean", "-f"], check=True, cwd=self.root_path, text=True)

        # Fetch all tags and checkout to current tag
        logging.info(f"Git - Checkout to {current_tag}")
        subprocess.run(["git", "fetch", "--tags"], check=True, cwd=self.root_path, text=True)
        subprocess.run(
            ["git", "checkout", f"tags/v{current_tag}"],
            check=True,
            cwd=self.root_path,
            text=True,
        )

        # Bouble-check if workspace is clean
        logging.info("Git - Checking for remaining changes")
        command = ["git", "status", "--porcelain"]
        result = subprocess.run(
            command,
            cwd=self.root_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        if result.stdout.strip():
            raise RuntimeError("Git workspace is not clean")

    def current_dir_is_network_path(self) -> bool:
        """Check if the current directory is on a network path.

        Returns:
            True if the path starts with '//' (UNC path), False otherwise.
        """
        return self.root_path.as_posix().startswith("//")

    def remove_virtual_environments(self) -> None:
        """Remove all existing virtual environments.

        This is used during reset operations to ensure a clean installation.
        """
        if not self.venvs_dir.exists():
            return

        logging.info(f"Removing virtual environments: {self.venvs_dir}")
        shutil.rmtree(self.venvs_dir)

    def setup_virtual_environments(self) -> None:
        """Create all required virtual environments from requirements files.

        Iterates through all requirements files and creates corresponding
        virtual environments if they don't already exist.
        """
        logging.info("Setup virtual environments")
        for requirement_file in self.requirements_files:
            self.setup_virtual_environment(requirement_file)

    def update_virtual_environments_packages(self) -> None:
        """Update packages in all virtual environments.

        Reinstalls packages from requirements files to ensure
        all environments are up to date.
        """
        logging.info("Update virtual environments packages")
        for requirement_file in self.requirements_files:
            self.update_virtual_environment_packages(requirement_file)

    def setup_virtual_environment(self, requirement_file: Path) -> None:
        """Create a virtual environment for a specific requirements file.

        Args:
            requirement_file: Path to the requirements file defining the environment.
        """
        venv_name = self.get_venv_name(requirement_file)
        venv_python_version = self.get_venv_python_version(requirement_file)
        venv_path = self.get_venv_path(venv_name, venv_python_version)

        if venv_path.exists():
            logging.info(f"Virtual environment already exists: {venv_path.name}")
            return

        logging.info(f"Setup virtual environment: {venv_name} ({venv_python_version})")
        command = [
            self.uv_path.as_posix(),
            "venv",
            venv_path.as_posix(),
            "--python",
            venv_python_version,
        ]
        subprocess.run(command, check=True)

    def update_virtual_environment_packages(self, requirement_file: Path) -> None:
        """Install or update packages in a virtual environment.

        Args:
            requirement_file: Path to the requirements file with package specifications.

        Raises:
            subprocess.CalledProcessError: If package installation fails.
        """
        venv_name = self.get_venv_name(requirement_file)
        venv_python_version = self.get_venv_python_version(requirement_file)
        venv_path = self.get_venv_path(venv_name, venv_python_version)
        python_exe = self.get_venv_python_exe(venv_path)

        logging.info(f"Installing packages to virtual environment: {venv_path.name}")
        command = [
            self.uv_path.as_posix(),
            "pip",
            "install",
            "-r",
            requirement_file.as_posix(),
            "--python",
            python_exe.as_posix(),
        ]
        subprocess.run(command, check=True)

    def get_venv_python_exe(self, venv_path: Path) -> Path:
        """Get the path to the Python executable in a virtual environment.

        Args:
            venv_path: Path to the virtual environment directory.

        Returns:
            Path to the Python executable (Scripts/python.exe on Windows).
        """
        return venv_path / "Scripts" / "python.exe"

    def get_venv_name(self, requirement_file: Path) -> str:
        """Extract the virtual environment name from a requirements file.

        The requirements file name should follow the format: name__version.txt

        Args:
            requirement_file: Path to the requirements file.

        Returns:
            The environment name (part before '__').
        """
        return requirement_file.stem.split("__")[0]

    def get_venv_python_version(self, requirement_file: Path) -> str:
        """Extract the Python version from a requirements file.

        The requirements file name should follow the format: name__version.txt
        where version uses underscores (e.g., 3_11_0).

        Args:
            requirement_file: Path to the requirements file.

        Returns:
            Python version string with dots (e.g., '3.11.0').
        """
        return requirement_file.stem.split("__")[1].replace("_", ".")

    def get_venv_path(self, venv_name: str, venv_python_version: str) -> Path:
        """Construct the path to a virtual environment directory.

        Args:
            venv_name: Name of the virtual environment.
            venv_python_version: Python version string (e.g., '3.11.0').

        Returns:
            Path to the virtual environment directory.
        """
        return self.venvs_dir / f"{venv_name}_{venv_python_version}"

    @property
    def uv_path(self) -> Path:
        """Get the path to the UV executable.

        Returns:
            Path to uv.exe in the bin directory.
        """
        return self.root_path / "bin" / "uv" / "uv.exe"

    @property
    def venvs_dir(self) -> Path:
        """Get the directory containing all virtual environments.

        Returns:
            Path to the venvs directory.
        """
        return self.root_path / "venvs"

    @property
    def requirements_dir(self) -> Path:
        """Get the directory containing requirements files.

        Returns:
            Path to the install/requirements directory.
        """
        return self.root_path / "conf" / "requirements"

    @property
    def requirements_files(self) -> List[Path]:
        """Get all requirements files in the requirements directory.

        Returns:
            List of paths to .txt files in the requirements directory.
        """
        return list(self.requirements_dir.glob("*.txt"))

    @property
    def current_tag(self) -> str:
        """Fetch the current version tag from the shared URL.

        Reads the URL from current_tag_url.txt and fetches the version string.

        Returns:
            Version tag string (without 'v' prefix).

        Raises:
            FileNotFoundError: If current_tag_url.txt doesn't exist.
            urllib.error.URLError: If the URL cannot be fetched.
            TimeoutError: If the request takes longer than 1 second.
        """
        path = self.root_path / "install" / "current_tag_url.txt"
        with path.open("r") as txt_file:
            url = txt_file.read().strip()

        with urlopen(url, timeout=1) as response:
            version = response.read().decode().strip()
        return version

    @property
    def core_python_exe(self) -> Path:
        """Get the Python executable from the core virtual environment.

        Returns:
            Path to python.exe in the core virtual environment.

        Raises:
            IndexError: If no core requirements file is found.
        """
        core_files = [file for file in self.requirements_files if file.name.startswith("core")]
        if not core_files:
            raise ValueError("No core requirements file found")

        core = core_files[0]
        venv_name = self.get_venv_name(core)
        venv_python_version = self.get_venv_python_version(core)
        venv_path = self.get_venv_path(venv_name, venv_python_version)
        return self.get_venv_python_exe(venv_path)

    def create_shortcuts(self) -> None:
        """Create Windows shortcuts for launching BluePepper.

        Creates two shortcuts:
        1. bluepepperConsole.lnk: Direct console launcher with console icon
        2. bluepepper.lnk: User-friendly launcher that runs hidden PowerShell

        The two-shortcut approach ensures proper icon display in Windows.

        Raises:
            subprocess.CalledProcessError: If shortcut creation fails.
        """
        script_path = self.root_path / "install" / "create_shortcut.py"

        # Create console shortcut
        console_shortcut_path = self.root_path / "bluepepperConsole.lnk"
        logging.info(f"Creating shortcut: {console_shortcut_path}")
        self._create_shortcut(
            script_path=script_path,
            shortcut_path=console_shortcut_path,
            icon_path=self.root_path / "bluepepper/gui/icons/console.ico",
            target=self.core_python_exe,
            arguments=f'{str(self.root_path / "main.py")} --shell',
        )

        # Create user-friendly shortcut
        shortcut_path = self.root_path / "bluepepper.lnk"
        logging.info(f"Creating shortcut: {shortcut_path}")
        self._create_shortcut(
            script_path=script_path,
            shortcut_path=shortcut_path,
            icon_path=self.root_path / "bluepepper/gui/icons/bluepepper.ico",
            target=self.core_python_exe,
            arguments=str(self.root_path / "main.py"),
        )

    def _create_shortcut(
        self,
        script_path: Path,
        shortcut_path: Path,
        icon_path: Path,
        target: Path,
        arguments: str,
    ) -> None:
        """Create a Windows shortcut using the UV runner.

        Args:
            script_path: Path to the create_shortcut.py script.
            shortcut_path: Path where the shortcut will be created.
            icon_path: Path to the icon file.
            target: Path to the target executable.
            arguments: Command-line arguments for the target.

        Raises:
            subprocess.CalledProcessError: If shortcut creation fails.
        """
        command = [
            self.uv_path.as_posix(),
            "run",
            "--active",
            script_path.as_posix(),
            "--path",
            str(shortcut_path),
            "--icon",
            str(icon_path),
            "--target",
            str(target),
            "--arguments",
            arguments,
        ]
        subprocess.run(command, check=True)


def init_logging(app: str) -> logging.Logger:
    """Initialize logging configuration for the application.

    Creates both console and file handlers with appropriate formatting.

    Args:
        app: Application name used for log file naming.

    Returns:
        Configured root logger instance.
    """
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s] %(message)s",
        "%H:%M:%S",
    )

    # Clear existing handlers
    logger.handlers = []

    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(os.environ["BLUEPEPPER_LOG_LEVEL"])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File handler for persistent logs
    path = get_log_path(app)
    path.parent.mkdir(exist_ok=True, parents=True)
    file_handler = logging.FileHandler(filename=path.as_posix())
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_log_path(app: str) -> Path:
    """
    Construct the path for log files based on root directory, date, and session ID.

    Args:
        app: Application name for organizing logs.

    Returns:
        Path to the log file.
    """
    root_path = Path(os.environ["BLUEPEPPER_ROOT"])
    now = datetime.now()
    day_str = now.strftime("%Y_%m_%d")
    sess_id = os.environ["BLUEPEPPER_SESSION_ID"]
    return root_path / ".logs" / day_str / app / f"{sess_id}.log"


def parse_arguments() -> Namespace:
    """Parse command-line arguments for the installer.

    Returns:
        Parsed arguments namespace with update_repository, update_packages,
        and reset flags.
    """
    parser = ArgumentParser(description="BluePepper installation and environment management system")
    parser.add_argument(
        "-ur",
        "--update_repository",
        action="store_true",
        help="Update git repository to current tag",
    )
    parser.add_argument(
        "-up",
        "--update_packages",
        action="store_true",
        help="Update packages in virtual environments",
    )
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="Remove existing virtual environments before installation",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    _main(
        update_repository=args.update_repository,
        update_packages=args.update_packages,
        reset=args.reset,
    )
