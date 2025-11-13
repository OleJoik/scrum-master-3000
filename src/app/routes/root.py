from fastapi import APIRouter
from app.routes.ui import ui_router

router = APIRouter()
router.include_router(ui_router, include_in_schema=False)
