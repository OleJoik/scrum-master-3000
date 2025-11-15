from enum import StrEnum

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class AppConfig(BaseSettings):
    log_level: LogLevel = LogLevel.INFO
    port: int = 8080
    host: str = "0.0.0.0"

    oidc_config_path: str = Field(default=...)
    oidc_client_id: str = Field(default=...)
    oidc_client_secret: SecretStr = Field(default=...)
    oidc_redirect_uri: str = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env")
