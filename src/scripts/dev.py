import uvicorn

from backend.bootstrap import setup_app
from backend.config import AppConfig
from scripts import esbuild, tailwind

config = AppConfig()
app = setup_app(config)


def main():
    with esbuild.watch():
        with tailwind.watch():
            uvicorn.run(
                "scripts.dev:app",
                host=config.host,
                port=config.port,
                log_level=config.log_level,
                reload=True,
            )


if __name__ == "__main__":
    main()
