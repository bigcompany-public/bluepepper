from dataclasses import dataclass


@dataclass(frozen=True)
class DomainConfig:
    # WARNING : Do not push sensitive data to the repository, use environment variables or keyring instead
    ldap_server: str = ""
