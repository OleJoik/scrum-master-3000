from fastapi import APIRouter
from fastapi.responses import HTMLResponse

import htpy as h


ui_router = APIRouter()


@ui_router.get("/")
async def hello():
    return HTMLResponse(h.html[h.body[h.main[h.p["Hello from scrum master"]]]])
