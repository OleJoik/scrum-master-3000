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
    port: int = 8755
    host: str = "0.0.0.0"

    session_secret: SecretStr = Field(default=...)

    app_base_uri: str = Field(default=...)

    oidc_config_path: str = Field(default=...)
    oidc_client_id: str = Field(default=...)
    oidc_client_secret: SecretStr = Field(default=...)
    oidc_signature_algorithm: str = Field(default=...)

    @property
    def oidc_redirect_uri(self) -> str:
        return f"{self.app_base_uri}/auth/callback"

    model_config = SettingsConfigDict(env_file=".env")
