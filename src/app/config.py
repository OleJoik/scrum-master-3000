from enum import StrEnum
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

    model_config = SettingsConfigDict(env_file=".env")
