from fastapi import FastAPI, Request

from app.config import AppConfig
from app.oidc import OidcConfig, oidc_config


def set_state(app: FastAPI, config: AppConfig):
    app.state._config = config
    app.state._oidc_config = oidc_config(config)


def get_config(request: Request) -> AppConfig:
    return request.app.state._config


def get_oidc_config(request: Request) -> OidcConfig:
    return request.app.state._oidc_config
