from enum import StrEnum
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse


SRC_DIRECTORY = Path("src") / "frontend" / "entrypoints"
REACT_DIRECTORY = ".react"


class EntryPoint(StrEnum):
    INDEX = "index.jsx"
    TEST_ENTRY = "testEntrypoint.tsx"


react_router = APIRouter()


def entrypoint_path(entrypoint: EntryPoint):
    return f"/js/{entrypoint.split('.')[0]}.js"


for entry in EntryPoint:

    @react_router.get(entrypoint_path(entry))
    async def _():
        return FileResponse(f".react/{entry.split('.')[0]}.js")


STYLES_PATH = "/styles.css"
STYLES_FILE = Path(".tailwind") / "styles.css"


@react_router.get(STYLES_PATH)
async def _():
    return FileResponse(STYLES_FILE)
