# Embedded FastAPI Server

## About The FastAPI Server

BluePepper has an embedded FastAPI server that starts when the application is launched. This allows you to run actions via web requests, letting you interact with BluePepper from outside (another DCC, another computer, etc.).

By default, the server runs on port 9999, but you can set a different port in the `conf/fastapi.py`:memo: configuration file.

=== "python"
    ```python
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class FastApiSettings:
        fastapi_port: int = 9999
    ```

!!! info
    You may open multiple instances of BluePepper, but only one FastAPI server can run at a time. Thus, the first BluePepper instance you open will handle all requests.

## Sending a Request

=== "BluePepper Client (Python)"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action(
        "run_app_function/show_toast",
        payload={"message": "Hello World"}
    )
    ```

=== "Python"
    ```python
    import requests

    requests.post(
        url="http://localhost:9999/run_app_function/show_toast",
        json={"message": "Hello World"}
    )
    ```

=== "Bash"
    ```
    curl -X POST "http://localhost:9999/run_app_function/show_toast" -H "Content-Type: application/json" -d '{"message": "Hello World"}'
    ```

=== "PowerShell"
    ```powershell
    Invoke-RestMethod -Uri "http://localhost:9999/run_app_function/show_toast" `
        -Method POST `
        -ContentType "application/json" `
        -Body '{"message": "hello world"}'
    ```

## Out Of The Box Actions

### Submitting a Batcher Job

!!! tip
    The batcher is basically a way to run any piece of python code, as all arguments needed to create the job shall be passed through the request's payload.

!!! warning
    Depending on your firewall's configuration, this can cause security issues. Use it wisely, and get in touch with your IT department to secure the FastAPI port.

=== "python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action(
        route="run_app_function/submit_batcher_job",
        payload={
            "name": "FastAPI Job",
            "description": "This job was submitted using a web request",
            "module": "bluepepper.toast",
            "func": "show_message_toast",
            "kwargs": {"message": "This job shows a toast"},
            "priority": 100,
            "notify_when_done": True,
            "notify_message": "FastAPI job is now done",
        },
    )
    ```

### Show Notification

=== "Python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action(
        "run_app_function/show_toast",
        payload={"message": "Hello World"}
    )
    ```

### Select Documents

=== "Python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action(
        "run_app_function/select_documents",
        payload={
            "entity": "asset",
            "document_ids": ["69e8e20947723886c7cb6869", "69e8e1a347723886c7cb6868"],
            "sender": "FastAPI",  # Optional
        },
    )
    ```

### Close BluePepper

=== "Python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action("run_app_function/close")
    ```

### Show BluePepper

=== "Python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action("run_app_function/show")
    ```

### Hide BluePepper

=== "Python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action("run_app_function/minimize")
    ```

### Set Active Page

=== "Python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action(
        "run_app_function/set_active_page",
        payload={"index": 1},  # 0=Launcher, 1=Browser, 2=Batcher, 3=EntityCreator
    )
    ```

### Reboot Computer

=== "Python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action("run_app_function/reboot")
    ```
