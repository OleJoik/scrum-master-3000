from fastapi import FastAPI

from app.config import AppConfig
from app.dependencies import set_state
from app.routes.root import router


def setup_app(config: AppConfig):
    app = FastAPI()

    app.include_router(router)

    set_state(app, config)

    return app
