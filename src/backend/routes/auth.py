from datetime import UTC, datetime
import secrets
from urllib.parse import urlencode

import htpy as h
import httpx
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

from backend.config import AppConfig
from backend.dependencies import get_config, get_oidc_config
from backend.oidc import OidcConfig

auth_router = APIRouter()


class UserIdentity(BaseModel):
    sub: str
    email: str
    exp: datetime
    token: str


async def verify_id_token(
    id_token: str, expected_nonce: str, oidc_config: OidcConfig, app_config: AppConfig
) -> UserIdentity:
    jwks_client = jwt.PyJWKClient(oidc_config.jwks_uri)

    signing_key = jwks_client.get_signing_key_from_jwt(id_token).key

    payload = jwt.decode(
        id_token,
        signing_key,
        algorithms=[app_config.oidc_signature_algorithm],
        audience=app_config.oidc_client_id,
    )

    if payload.get("nonce") != expected_nonce:
        raise Exception("Invalid nonce")

    return UserIdentity.model_validate({**payload, "token": id_token})


async def authenticate(request: Request):
    user = request.session.get("user")
    if user:
        identity = UserIdentity.model_validate(user)
        if identity.exp > datetime.now(tz=UTC):
            return

    next_url = request.url.path
    raise HTTPException(303, headers={"Location": f"/auth/login?next={next_url}"})


@auth_router.get("/auth/login")
async def login(
    request: Request,
    next: str | None = None,
    oidc_config: OidcConfig = Depends(get_oidc_config),
    app_config: AppConfig = Depends(get_config),
):
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    request.session["oidc"] = {
        "state": state,
        "nonce": nonce,
        "next": next,
    }

    params = {
        "client_id": app_config.oidc_client_id,
        "redirect_uri": app_config.oidc_redirect_uri,
        "response_type": "code",
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
    }

    redirect_url = f"{oidc_config.authorization_endpoint}?{urlencode(params)}"

    return RedirectResponse(redirect_url, status_code=303)


@auth_router.get("/auth/callback")
async def callback(
    code: str,
    state: str,
    request: Request,
    oidc_config: OidcConfig = Depends(get_oidc_config),
    app_config: AppConfig = Depends(get_config),
):
    stored = request.session.get("oidc")
    if not stored:
        raise HTTPException(400, "Missing OIDC session")

    if state != stored["state"]:
        raise HTTPException(400, "Invalid state")

    token_data = {
        "grant_type": "authorization_code",
        "client_id": app_config.oidc_client_id,
        "client_secret": app_config.oidc_client_secret.get_secret_value(),
        "code": code,
        "redirect_uri": app_config.oidc_redirect_uri,
    }

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(oidc_config.token_endpoint, data=token_data)
        token_resp.raise_for_status()

    tokens = token_resp.json()
    id_token = tokens["id_token"]

    verified_id_token = await verify_id_token(
        id_token, stored["nonce"], oidc_config, app_config
    )

    next_url = stored.get("next")
    request.session.pop("oidc", None)

    request.session["user"] = verified_id_token.model_dump(mode="json")

    if next_url:
        return RedirectResponse(next_url)

    return RedirectResponse(app_config.app_base_uri)


@auth_router.get("/auth/logout")
async def logout(
    request: Request,
    oidc_config: OidcConfig = Depends(get_oidc_config),
    app_config: AppConfig = Depends(get_config),
):
    id_token = request.session.get("user", {}).get("token")
    request.session.clear()

    params = urlencode(
        {
            "id_token_hint": id_token,
            "post_logout_redirect_uri": app_config.app_base_uri,
        }
    )

    logout_url = f"{oidc_config.end_session_endpoint}?{params}"
    return RedirectResponse(logout_url)
