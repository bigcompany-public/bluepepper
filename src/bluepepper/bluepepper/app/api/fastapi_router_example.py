"""Example FastAPI router demonstrating HTTP request patterns.

This module provides example endpoints to illustrate different ways to pass
data in HTTP requests: query parameters vs request payloads.
"""

from bluepepper.core import version
from fastapi import APIRouter
from pydantic import BaseModel

router_example = APIRouter()


@router_example.get("/example/get_version")
async def get_version() -> str:
    """Return the currently running version of BluePepper.

    Returns:
        str: The version string from bluepepper.core.
    """
    return version


@router_example.post("/example/params")
async def say_hello_params(name: str) -> str:
    """Greet a user by name using query parameters.

    Query parameters are key-value pairs appended to the URL (?name=John).

    Pros:
        - Simple and readable in URLs
        - Easy to bookmark or share
        - Cached by browsers automatically

    Cons:
        - Limited length (typically ~2000 characters)
        - Visible in browser history and logs
        - Not suitable for sensitive data (passwords, tokens)
        - Not ideal for complex/nested data structures

    Args:
        name: The person's name to greet.

    Returns:
        str: A greeting message.
    """
    return f"Hello {name}"


class ExampleRequest(BaseModel):
    """Request payload for say_hello_payload endpoint.

    Attributes:
        name: The person's name.
        age: The person's age.
    """

    name: str
    age: int


@router_example.post("/example/payload")
async def say_hello_payload(payload: ExampleRequest) -> str:
    """Greet a user with details using a request payload.

    Request payloads are sent in the HTTP body as JSON/form data.

    Pros:
        - No size limitations (can handle large data)
        - Secure (hidden from URLs and logs by default)
        - Perfect for sensitive data (passwords, tokens)
        - Can contain complex nested structures

    Cons:
        - Not cacheable by standard browser caching
        - Less human-readable in debugging
        - Requires proper Content-Type headers

    Args:
        payload: The request body containing name and age.

    Returns:
        str: A greeting message with age information.
    """
    return f"Hello {payload.name} (age: {payload.age})"


@router_example.post("/example/params_and_payload")
async def say_hello_params_and_payload(payload: ExampleRequest, country: str) -> str:
    """Greet a user combining both parameters and payload.

    FastAPI automatically routes data: BaseModel instances come from the request body
    (in this example "ExampleRequest"), while other arguments come from query parameters.

    Args:
        payload: The request body (name and age).
        country: Query parameter for the user's country.

    Returns:
        str: A greeting message including all details.
    """
    return f"Hello {payload.name} (age: {payload.age}). Greetings from {country}"
