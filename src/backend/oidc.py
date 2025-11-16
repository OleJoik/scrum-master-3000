import httpx
from pydantic import BaseModel

from backend.config import AppConfig


class OidcConfig(BaseModel):
    authorization_endpoint: str
    token_endpoint: str
    jwks_uri: str
    end_session_endpoint: str


def oidc_config(config: AppConfig) -> OidcConfig:
    return OidcConfig.model_validate(httpx.get(config.oidc_config_path).json())
