"""
This module provides a client for sending requests to the BluePepper FastAPI server. It can be used to trigger actions
on bipipe's main application.
The client can be run from the command line, allowing users to easily interact with the FastAPI server
"""

import ast
import json
import logging
from argparse import ArgumentParser
from typing import Callable

import requests
from bluepepper.core import init_logging
from requests.exceptions import HTTPError
from requests.models import Response


def run_bluepepper_app_action(
    route: str,
    request_type: str = "post",
    params: dict | None = None,
    payload: dict | None = None,
    host: str = "",
    port: int = 0,
):
    """
    Send a request to the BluePepper FastAPI server.
    arguments:
    - route: API route to send the request to (e.g., "/run_app_function/close")
    - request_type: HTTP method to use for the request (default: "post")
    - params: Optional query parameters to include in the request
    - payload: Optional JSON payload to include in the request
    - host: Optional host to send the request to (default: "127.0.0.1")
    - port: Optional port to send the request to (default: Settings.fastapi_port)
    """
    # Get default host/port
    host = host or "127.0.0.1"
    port = port or Settings.fastapi_port

    # Format URL
    route = route.lstrip("/")
    url = f"http://{host}:{port}/{route}"

    # Format params/payload
    params = params or {}
    payload = payload or {}

    # Run request
    request_callback: Callable = getattr(requests, request_type)
    response: Response = request_callback(url, params=params, json=payload, timeout=2)
    if not response.ok:
        message = f"BluePepper FastAPI Server returned error {response.status_code}\n"
        message += json.dumps(response.json()["detail"], indent=4)
        raise HTTPError(message)
    logging.info(f"BluePepper FastAPI Server response: {response.json()}")


if __name__ == "__main__":
    init_logging("fastApiClient")
    parser = ArgumentParser()
    parser.add_argument("-r", "--route", required=True, type=str)
    parser.add_argument("-rt", "--request_type", required=False, type=str, default="post")
    parser.add_argument("-ho", "--host", required=False, type=str)
    parser.add_argument("-p", "--port", required=False, type=int)
    parser.add_argument("-pa", "--params", required=False)
    parser.add_argument("-pl", "--payload", required=False)
    args = parser.parse_args()
    params = ast.literal_eval(args.params) if args.params else None
    payload = ast.literal_eval(args.payload) if args.payload else None

    run_bluepepper_app_action(
        route=args.route,
        request_type=args.request_type,
        params=params,
        payload=payload,
        host=args.host,
        port=args.port,
    )
