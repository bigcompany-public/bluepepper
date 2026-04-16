"""Module for initializing and configuring application logging."""

import logging
import os
from datetime import datetime
from pathlib import Path


def init_logging(app: str) -> logging.Logger:
    """
    Initialize and configure the logging system.

    Arguments:
        app: Application name used for log file organization.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s", "%H:%M:%S")

    # Stream handler with level from environment
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(os.environ.get("BLUEPEPPER_LOG_LEVEL", "INFO"))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File handler for persistent logging
    log_path = get_log_path(app)
    log_path.parent.mkdir(exist_ok=True, parents=True)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(f"Logging initialized. Log file at: {log_path.as_posix()}")

    return logger


def get_log_path(app: str) -> Path:
    """
    Determine the log file path for the application.

    Checks BLUEPEPPER_LOG_PATH environment variable first for custom paths,
    otherwise constructs a dated path under BLUEPEPPER_ROOT.

    Arguments:
        app: Application name for log file organization.

    Returns:
        Path object pointing to the log file.

    Raises:
        KeyError: If required environment variables are missing.
    """
    if custom_path := os.environ.get("BLUEPEPPER_LOG_PATH"):
        return Path(custom_path)

    root_path = Path(os.environ["BLUEPEPPER_ROOT"])
    day_str = datetime.now().strftime("%Y_%m_%d")
    sess_id = os.environ["BLUEPEPPER_SESSION_ID"]

    return root_path / f".logs/{day_str}/{app}/{sess_id}.log"


if __name__ == "__main__":
    logger = init_logging("test")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
