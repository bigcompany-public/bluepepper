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