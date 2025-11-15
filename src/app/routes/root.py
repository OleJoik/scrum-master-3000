from fastapi import APIRouter, Depends
from app.routes.auth import authenticate, auth_router
from app.routes.ui import ui_router

router = APIRouter()

authenticated_routes = APIRouter(dependencies=[Depends(authenticate)])
authenticated_routes.include_router(ui_router, include_in_schema=False)

router.include_router(authenticated_routes)
router.include_router(auth_router, include_in_schema=False)
