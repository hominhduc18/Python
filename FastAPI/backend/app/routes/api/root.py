# import sys
# sys.path.append(".")

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.frontend import templates
from app.routes import login_manager

router = APIRouter()



@router.get("/dashboard",)
async def dashboard(request: Request, user = Depends(login_manager.manager)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "DashBoard"})

@router.get("/",)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

