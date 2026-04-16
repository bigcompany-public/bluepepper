from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    host: str = "127.0.0.1"
    port: int = 27017
    database_name: str = "bluepepper"

    # If identification is not needed, set user and password to None
    # WARNING : never commit hard-written credentials, use environment variables or keyring instead
    user: str | None = None
    password: str | None = None
