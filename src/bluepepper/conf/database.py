from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    """
    WARNING : never commit sensible data, use environment variables or keyring instead
    """

    database_name: str = "bluepepper"
    mode: str = "local"  # host-port, uri, or local

    # Method 1 : Host + Port
    # If identification is not needed, set user and password to None
    host: str = "127.0.0.1"
    port: int = 27017
    user: str | None = None
    password: str | None = None

    # Method 2 : URI
    uri: str | None = "mongodb+srv://user:password@myMongoDbCluster.com/?retryWrites=true&w=majority"

    # Method 3 : Local
    # Does not need any configuration
