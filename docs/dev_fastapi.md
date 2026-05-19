# Embedded FastAPI Server

BluePepper has an embedded FastAPI server, that starts when BluePepper is launched. This allows to run actions using web requests, meaning that you can interact with BluePepper from the outside (another DCC, another computer, and so on)

By default, the server runs on port 9999, but you may set your own port in the `conf/fastapi.py`:memo: configuration file.

=== "python"
    ```python
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class FastApiSettings:
        fastapi_port: int = 9999
    ```

## Sending a Request

*Coming Soon*

### Submitting a Batcher Job Using FastAPI

It is also possible to submit a job using a web request. All arguments needed to create the job shall be passed through the request's payload.
Here is an example using BluePepper's builtin client:

=== "python"
    ```python
    from bluepepper.app.api.fastapi_client import run_bluepepper_app_action

    run_bluepepper_app_action(
        route="run_app_function/submit_batcher_job",
        payload={
            "name": "FastAPI Job",
            "description": "This job was submitted using a web request",
            "module": "pprint",
            "func": "pprint",
            "kwargs": {"object": "Hello World"},
            "priority": 100,
            "notify_when_done": True,
            "notify_message": "FastAPI job is now done",
        },
    )
    ```