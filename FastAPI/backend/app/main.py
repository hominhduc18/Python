import sys
sys.path.append(".")
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, WebSocket, Security
from app.routes.api_v1 import api_router
from app.frontend import templates
from app.routes import login_manager
from app.exceptions import exceptions
import time
import os
app = FastAPI()
directory = "/home/teca/workspace/app_0.2/frontend/static"
app.mount("/static", StaticFiles(directory=directory), name="static")

app.mount("/css", StaticFiles(directory=directory+"/css"), name="css")
app.mount("/js", StaticFiles(directory=directory+"/js"), name="js")
app.mount("/fontawesome-free-6.1.1-web", StaticFiles(directory=directory+"/fontawesome-free-6.1.1-web"), name="fontawesome-free-6.1.1-web")
app.mount("/img", StaticFiles(directory=directory+"/img"), name="img")


directory_admin = "/home/teca/workspace/app_0.2/frontend/templates/admin/static"
app.mount("/static-admin", StaticFiles(directory=directory_admin), name="static-admin")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["Process-Time"] = str(process_time)
    return response

from app.exceptions import exceptions

app.include_router(api_router)


app.add_exception_handler(exceptions.NotAuthenticatedException, exceptions.not_authenticated_exception_handler)
app.add_exception_handler(exceptions.LoginException, exceptions.login_exception_handler)
app.add_exception_handler(exceptions.UserNotPermissionException, exceptions.user_not_permission_exception_handler)
app.add_exception_handler(exceptions.HTTP_401_UNAUTHORIZED, exceptions.unauthorized_error_exception)
app.add_exception_handler(exceptions.HTTP_500_INTERNAL_SERVER_ERROR, exceptions.server_error_exception)
app.add_exception_handler(exceptions.HTTP_422_UNPROCESSABLE_ENTITY, exceptions.unprocessable_entity_error_exception)

import asyncio
from random import randint

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # cpu = CPU(**await test())
            led_lst = [False]*14
            for i in range(randint(0,13)):
                led_lst[randint(0,13)] = True
            await asyncio.sleep(0.2)
            cpu = {"CPU": randint(60, 75), "leds": led_lst}
            await websocket.send_json(cpu)
            await asyncio.sleep(1.3)
        except Exception as e:
            print(e)
            break

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(BASE_DIR)
