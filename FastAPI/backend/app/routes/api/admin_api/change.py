from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException,Request, status, Form, Security, WebSocket
from fastapi.responses import RedirectResponse
from app.routes import login_manager
from app.schemas import User
from app.frontend import templates
from app.models import models
from app.database import crud
from app.database import database
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timezone
import asyncio
from app.system import time_system
router = APIRouter()


@router.get("/time")
async def admin_page_change_time(request: Request,  user: User.User = Security(login_manager.manager, scopes=["admin"])):
    # print(time_now)
    list_time_zone = list(time_system.TIME_ZONE.keys())
    return templates.TemplateResponse("/admin/changeTime.html", context={"request":request, "title": "Admin", "admin": user.username, "TIME_ZONES": list_time_zone})

@router.post("/time")
async def post_admin_page_change_time(request: Request,  user: User.User = Security(login_manager.manager, scopes=["admin"]),
    time_zone = Form(...)):
    # print(time_zone)
    #  "Countrie": time_system.TIME_ZONE[""]
    if time_zone != "":
        await time_system.set_timezone(time_zone)
    # print(time_system.TIME_ZONE[time_zone])
    resp = RedirectResponse("/admin/change/time", status_code=status.HTTP_302_FOUND)
    return resp


@router.websocket_route("/time")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # now = datetime.now()
            # time_now = f'{datetime.now():%d-%m-%Y %H:%M:%S%z}'
            # local_now = now.astimezone()
            # local_tz = local_now.tzinfo
            # local_tzname = local_tz.tzname(local_now)
            # utc_now = local_tzname
            
            time = await time_system.get_system_time_now()
            timezone = await time_system.get_system_time_zone()
            # print(timezone)
            # print(time_now)
            system_info = {"time": time, "utc": timezone["time_zone"]+" "+timezone["utc"], "location": time_system.TIME_ZONE[timezone["time_zone"]]}
            # print(type(system_info))
            await websocket.send_json(system_info)
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            break

import socket
from app.system.ip_system import IP
import ipaddress
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

@router.get("/ip")
async def admin_page_change_ip(request: Request, user: User.User = Security(login_manager.manager, scopes=["admin"])):
    try:
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_address = s.getsockname()[0]
    except:
        local_ip_address = "0.0.0.0"
    return templates.TemplateResponse("/admin/changeIP.html", context={"request":request, "title": "Admin", "admin": user.username,"current_ip": local_ip_address})


@router.post("/ip",)
async def post_admin_page_change_time(request: Request,  user: User.User = Security(login_manager.manager, scopes=["admin"]),
    ip = Form(default=None), prefix = Form(default="/24")):
    if ip == None or prefix == None:
        raise HTTPException(status_code=422)

    try:
        check_ip = ipaddress.ip_address(ip)
        new_ip = ip+prefix
        IP.change_ip(new_ip)
        IP.update_ip()
        return RedirectResponse("/admin/change/ip", status_code=302)
    except:
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_address = s.getsockname()[0]
        return templates.TemplateResponse("/admin/changeIP.html", 
            context={"request":request, "title": "Admin", "admin": user.username,"current_ip": local_ip_address, "check": "Đổi ip không thành công"},
            status_code=417)
