import logging
import socket
import threading

import uvicorn
from bluepepper.app.api.fastapi_router_browser import router_browser
from bluepepper.app.api.fastapi_router_example import router_example
from bluepepper.core import init_logging
from conf.fastapi import FastApiSettings
from fastapi import FastAPI

app = FastAPI()
app.include_router(router_example)
app.include_router(router_browser)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    Starts the FastAPI server over the specified host/port.

    Args:
        host (str): The host address for the server. Defaults to "0.0.0.0".
        port (int): The port number for the server. Defaults to 8000.
    """
    uvicorn.run(app, host=host, port=port)


def is_port_in_use(host: str, port: int, timeout: float = 0.1) -> bool:
    """
    Check if a port is in use on the given host with a timeout.

    Args:
        host (str): The hostname to check.
        port (int): The port to check.
        timeout (float): The timeout for the connection check.

    Returns:
        bool: True if the port is in use, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        return result == 0


def run_server_as_daemon(host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    Starts the FastAPI server as a daemon over the specified host/port.

    Args:
        host (str): The host address for the server. Defaults to "0.0.0.0".
        port (int): The port number for the server. Defaults to 8000.
    """
    if is_port_in_use(host=host, port=port):
        logging.warning(f"The FastAPI server is already running on port {port}. Aborting...")
        return

    server_thread = threading.Thread(target=run_server, kwargs={"port": port, "host": host}, daemon=True)
    server_thread.start()


if __name__ == "__main__":
    init_logging("fastapiServer")
    run_server(host="0.0.0.0", port=FastApiSettings.fastapi_port)
