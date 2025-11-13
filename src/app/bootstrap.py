from fastapi import FastAPI

from app.routes.root import router


def setup_app():
    app = FastAPI()

    app.include_router(router)

    return app
