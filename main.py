"""
BluePepper Igniter Module

This main script sets up subprocesses in which BluePepper runs in the proper environment.
Imports MUST NOT contain any module or package with dependencies so any distribution
of Python can run this script.
"""

import ctypes
import logging
import os
import subprocess
import sys
import traceback
import uuid
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from typing import NoReturn

from conf.project import ProjectSettings
from install.install import BluePepperInstaller


class BluePepperIgniter:
    """
    Main orchestrator for BluePepper initialization and environment setup.

    This class handles environment configuration, GUI/shell launching, and
    manages the BluePepper session lifecycle.

    Attributes:
        uuid: Unique identifier for this igniter instance
        timestamp: Creation timestamp for session tracking
        root_dir: Root directory of the BluePepper installation
        shell: Whether to open a shell instead of GUI
        console: Whether to open console in a new window
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        installer: BluePepperInstaller instance for managing installations
    """

    def __init__(self, shell: bool = False, console: bool = False, log_level: str = "info") -> None:
        """
        Initialize the BluePepper igniter.

        Args:
            shell: If True, opens a shell instead of the GUI
            console: If True, opens PowerShell in a new window
            log_level: Logging level (debug, info, warning, error)
        """
        self.uuid: str = uuid.uuid4().hex
        self.timestamp: datetime = datetime.now()
        self.root_dir: Path = Path(__file__).resolve().parent
        self.shell: bool = shell
        self.console: bool = console
        self.log_level: str = log_level.upper()
        self.installer: BluePepperInstaller = BluePepperInstaller()

    def ignite(self) -> None:
        """
        Start the BluePepper application.

        Sets up environment variables, initializes logging, and launches
        either the shell or GUI depending on configuration.
        """
        init_logging("igniter")
        logging.info("Welcome to BluePepper Igniter")
        self.set_environment_variables()
        if self.shell:
            self.open_shell()
        else:
            self.open_gui()

    def set_environment_variables(self) -> None:
        """
        Set all required BluePepper environment variables.

        Iterates through the bluepepper_env dictionary and sets each
        key-value pair as an environment variable.
        """
        for key, value in self.bluepepper_env.items():
            logging.info(f"Setting environment variable : {key}={value}")
            os.environ[key] = value

    def update(self) -> None:
        """
        Update the BluePepper repository and packages.

        Creates a new installer instance configured for updates and
        runs the installation process.
        """
        installer: BluePepperInstaller = BluePepperInstaller(update_repository=True, update_packages=True)
        installer.install()

    @property
    def must_update(self) -> bool:
        """
        Check if BluePepper needs to be updated.

        Returns:
            True if the .editable_mode file does not exist, indicating
            that an update is required.
        """
        frozen_file: Path = Path(__file__).parent / ".editable_mode"
        return not frozen_file.exists()

    def open_shell(self) -> NoReturn:
        """
        Open a PowerShell terminal with BluePepper environment variables.

        If console mode is enabled, PowerShell opens in a new window.
        Otherwise, it runs in the current terminal. This method exits
        the Python process after the shell closes.

        Raises:
            SystemExit: Always exits after PowerShell process completes
        """
        if self.must_update:
            self.update()

        logging.info("Opening BluePepper Shell")
        activate_script = self.installer.core_python_exe.parent / "activate.ps1"
        if self.console:
            process: subprocess.Popen[bytes] = subprocess.Popen(
                [
                    "powershell",
                    "-Command",
                    f"Start-Process powershell -ArgumentList '-NoExit', '-File', '{activate_script.as_posix()}'",
                ],
                cwd=self.root_dir.as_posix(),
            )
        else:
            process = subprocess.Popen(
                ["powershell", "-NoExit", "-File", activate_script.as_posix()],
                cwd=self.root_dir.as_posix(),
            )
        sys.exit(process.wait())

    @property
    def bluepepper_env(self) -> dict[str, str]:
        """
        Get BluePepper environment variables.

        Returns:
            Dictionary mapping environment variable names to their values,
            including virtual environment path, log level, root directory,
            session ID, console flag, and Python path.
        """
        return {
            # Enforce the virtual environment to use for script execution
            "VIRTUAL_ENV": str(self.installer.core_python_exe.parent.parent),
            "BLUEPEPPER_LOG_LEVEL": self.log_level,
            "BLUEPEPPER_ROOT": self.root_dir.as_posix(),
            "BLUEPEPPER_SESSION_ID": self.get_session_id(),
            "BLUEPEPPER_CONSOLE": str(int(self.console)),
            "PYTHONPATH": self.root_dir.as_posix(),
        }

    def open_gui(self) -> None:
        """
        Launch the BluePepper graphical user interface.

        Uses uv to run the Qt application in the configured virtual
        environment. Includes the --update flag if updates are needed.

        Raises:
            subprocess.CalledProcessError: If the GUI subprocess fails
        """
        logging.info("Opening BluePepper Graphical User Interface")
        # Launch the application using the uv run command
        command: list[str] = [self.installer.uv_path.as_posix(), "run"]

        # Run in the virtual environment defined by the "VIRTUAL_ENV" environment variable
        command += ["--active"]

        # Run the main event loop of the qt app
        open_app_script: Path = self.root_dir / "bluepepper/app/open_app.py"
        command += [open_app_script.as_posix()]
        if self.must_update:
            command += ["--update"]

        subprocess.run(command, check=True, cwd=self.root_dir.as_posix())

    def get_session_id(self) -> str:
        """
        Generate a unique session identifier.

        Returns:
            Session ID string formatted as YYYY_MM_DD_HH_MM_SS_{uuid}
        """
        return self.timestamp.strftime("%Y_%m_%d_%H_%M_%S") + f"_{self.uuid}"


def init_logging(app: str) -> logging.Logger:
    """
    Initialize logging configuration for BluePepper.

    Sets up both console and file logging handlers with appropriate
    formatting and log levels.

    Args:
        app: Name of the application component being logged

    Returns:
        Configured root logger instance
    """
    logger: logging.Logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter: logging.Formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s", "%H:%M:%S")

    # Clear existing handlers
    logger.handlers = []

    # Stream handler
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(os.environ["BLUEPEPPER_LOG_LEVEL"])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File handler
    path: Path = get_log_path(app)
    path.parent.mkdir(exist_ok=True, parents=True)
    file_handler: logging.FileHandler = logging.FileHandler(filename=path.as_posix())
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_log_path(app: str) -> Path:
    """
    Determine the log file path for the application.
    Constructs a path based on root directory, date, and session ID.

    Args:
        app: Name of the application component

    Returns:
        Path object pointing to the log file location
    """
    root_path: Path = Path(os.environ["BLUEPEPPER_ROOT"])
    now: datetime = datetime.now()
    day_str: str = now.strftime("%Y_%m_%d")
    sess_id: str = os.environ["BLUEPEPPER_SESSION_ID"]
    log_path: Path = root_path / f".logs/{day_str}/{app}/{sess_id}.log"
    return log_path


def configure_console_window() -> None:
    """
    Configure the Windows console window appearance.

    Sets the console title, icon, and app user model ID for proper
    Windows taskbar integration.

    Note:
        This function is Windows-specific and uses ctypes to call
        Win32 API functions.
    """
    ctypes.windll.kernel32.SetConsoleTitleW(f"BluePepper - {ProjectSettings.project_name} (Console)")

    hwnd: int = ctypes.windll.kernel32.GetConsoleWindow()
    icon: Path = Path(__file__).with_name("icon.ico")
    hicon: int = ctypes.windll.user32.LoadImageW(
        None,
        icon.as_posix(),
        1,
        0,
        0,
        0x00000010,  # IMAGE_ICON  # LR_LOADFROMFILE
    )
    WM_SETICON: int = 0x0080
    ICON_BIG: int = 1
    ICON_SMALL: int = 0
    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)

    # Set app ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"bluepepper.{ProjectSettings.project_name}")


def main():
    configure_console_window()
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--shell",
        required=False,
        action="store_true",
        help="Opens a shell instead of opening the launcher",
    )
    parser.add_argument(
        "-c",
        "--console",
        required=False,
        action="store_true",
        help="Pops a shell open to help for debugging",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="info",
        help="Log level. Available options are : debug, info, warning, error",
    )
    args: Namespace = parser.parse_args()

    try:
        bluepepper: BluePepperIgniter = BluePepperIgniter(
            shell=args.shell, console=args.console, log_level=args.log_level
        )
        bluepepper.ignite()
    except Exception:
        logging.error(traceback.format_exc())
        input("Press any key to continue...")


if __name__ == "__main__":
    main()
