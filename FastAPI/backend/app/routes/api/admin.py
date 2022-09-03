from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException,Request, status, Form, Security, WebSocket
from app.routes import login_manager
from app.schemas import User
from app.frontend import templates
from app.models import models
from app.database import crud
from app.database import database
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import asyncio
router = APIRouter()


@router.get("/")
async def admin_page(request: Request,
            db: Session = Depends(login_manager.get_database), user: User.User = Security(login_manager.manager, scopes=["admin"])):
    return templates.TemplateResponse("/admin/index.html", context={"request":request, "title": "Admin", "admin": user.username})

@router.get("/user-manager")
async def admin_page_get(request: Request,
            db: Session = Depends(login_manager.get_database), user: User.User = Security(login_manager.manager, scopes=["admin"])):
    users : List[User.User] = crud.get_all_user(db=db) 

    users_public = list()
    for u in users:
        permission = str()
        for i in u.role.role_permission:
            permission += i.permission.description+' '
        if u.last_login:
            last_login = f'{u.last_login:%d-%m-%Y %H:%M:%S%z}'
        else:
            last_login = None
        user_public = User.UserPublic(id = u.id, username=u.username, last_login=last_login, role=u.role.role, permission=permission.strip(" "))
        users_public.append(user_public)

    return templates.TemplateResponse("/admin/managerUser.html", context={"request": request, "title": "Admin", "users": users_public, "admin": user.username})

@router.get("/system")
async def admin_page_test(request: Request, user: User.User = Security(login_manager.manager, scopes=["admin"])):
    return templates.TemplateResponse("/admin/system.html", context={"request":request, "title": "Admin", "admin": user.username})

from app.system import system

@router.websocket_route("/sys")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            system_info = await system.get_system_info()

            # print(type(system_info['ram']))
            await websocket.send_json(system_info)
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            break
# @router.get("/admin/change-password")

from app.routes.api.admin_api import change

router.include_router(change.router, prefix="/change")