from fastapi import APIRouter, Depends
from backend.routes.react import react_router
from backend.routes.auth import authenticate, auth_router
from backend.routes.ui import ui_router

router = APIRouter()

authenticated_routes = APIRouter(dependencies=[Depends(authenticate)])
authenticated_routes.include_router(ui_router, include_in_schema=False)
authenticated_routes.include_router(react_router, include_in_schema=False)

router.include_router(authenticated_routes)
router.include_router(auth_router, include_in_schema=False)
