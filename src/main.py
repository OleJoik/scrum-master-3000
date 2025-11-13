import uvicorn

from app.bootstrap import setup_app
from app.config import AppConfig

config = AppConfig()
app = setup_app()


def main():
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level)


if __name__ == "__main__":
    main()
