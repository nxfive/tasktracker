from pydantic import BaseSettings, PostgresDsn, SecretStr
from enum import Enum
from typing import Any


class EnvState(str, Enum):
    dev = "dev"
    prod = "prod"
    test = "test"


class BaseAppSettings(BaseSettings):
    env_state: EnvState = EnvState.prod

    class Config:
        env_file = ".env"


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    title: str = "Tasktracker App"
    version: str = "0.0.0"
    database_url: PostgresDsn
    secret_key: SecretStr

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        print(self.database_url)
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_url": self.openapi_url,
            "title": self.title,
            "version": self.version,
        }

    class Config:
        validate_assignment = True
