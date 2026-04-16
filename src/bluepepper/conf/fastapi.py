from dataclasses import dataclass


@dataclass(frozen=True)
class FastApiSettings:
    fastapi_port: int = 9999
