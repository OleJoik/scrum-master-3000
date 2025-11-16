from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.config import AppConfig
from backend.dependencies import set_state
from backend.routes.root import router


def setup_app(config: AppConfig):
    app = FastAPI()
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.session_secret.get_secret_value(),
    )

    app.include_router(router)

    set_state(app, config)

    return app
