import sys
sys.path.append(".")
from fastapi import APIRouter
from app.routes.api import root, auth, admin
api_router = APIRouter()
api_router.include_router(root.router, tags=["root"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
# api_router.add_api_websocket_route("/sys")
