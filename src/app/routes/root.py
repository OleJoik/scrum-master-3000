from fastapi import APIRouter, Depends
from app.routes.auth import authenticate
from app.routes.ui import ui_router

router = APIRouter(dependencies=[Depends(authenticate)])
router.include_router(ui_router, include_in_schema=False)
