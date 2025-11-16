import uvicorn

from backend.bootstrap import setup_app
from backend.config import AppConfig

config = AppConfig()
app = setup_app(config)


def main():
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level)


if __name__ == "__main__":
    main()
