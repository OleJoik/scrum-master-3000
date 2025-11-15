from fastapi import APIRouter, Depends, HTTPException

from app.config import AppConfig
from app.dependencies import get_config, get_oidc_config
from app.oidc import OidcConfig


auth_router = APIRouter()


async def authenticate(
    oidc_config: OidcConfig = Depends(get_oidc_config),
    app_config: AppConfig = Depends(get_config),
):
    _ = app_config.oidc_client_id

    params = {
        "client_id": app_config.oidc_client_id,
        "redirect_uri": app_config.oidc_redirect_uri,
        "response_type": "code",
        "scope": "openid profile email",
        # Optional:
        # "audience": app_config.oidc_audience,
    }

    raise HTTPException(303, headers={"Location": oidc_config.authorization_endpoint})
