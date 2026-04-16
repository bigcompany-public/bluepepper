from typing import Any

from bluepepper.app.api.fastapi_bridge import fastapi_bridge
from fastapi import APIRouter, Body

router_browser = APIRouter()


@router_browser.post("/run_app_function/{function_name}")
async def run_app_function(
    function_name: str, payload: dict[str, Any] = Body(...)
) -> dict:
    """Execute an app function dynamically.

    This endpoint allows calling arbitrary functions from the bluepepper app. The
    function name is specified in the URL route, while keyword arguments are
    passed via the request body as a dictionary (we use `dict[str, Any]` instead
    of a Pydantic model to accommodate dynamic function signatures).

    Args are injected into the payload and emitted through the fastapi_bridge.
    """
    payload["_function"] = function_name
    fastapi_bridge.payload.emit(payload)
    return {"message": "Running app function", "body": payload}
