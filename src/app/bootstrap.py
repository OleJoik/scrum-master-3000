from fastapi import FastAPI

from app.config import AppConfig
from app.dependencies import set_state
from app.routes.root import router
from starlette.middleware.sessions import SessionMiddleware


def setup_app(config: AppConfig):
    app = FastAPI()
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.session_secret.get_secret_value(),
    )

    app.include_router(router)

    set_state(app, config)

    return app
