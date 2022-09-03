from fastapi import HTTPException, status
from starlette.requests import Request
from fastapi.responses import RedirectResponse
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from app.frontend import templates

async def server_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/500.html",
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        context={"request": request},
    )

async def unprocessable_entity_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/422.html",
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        context={"request": request},
    )


async def unauthorized_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse("errors/401.html", status_code=HTTP_401_UNAUTHORIZED, context={"request": request})


class NotAuthenticatedException(Exception):
    status_code = status.HTTP_307_TEMPORARY_REDIRECT
    pass

async def not_authenticated_exception_handler(request, exception:NotAuthenticatedException):
    return RedirectResponse("/login", status_code=exception.status_code) # 302 khong loi voi cac chuc nang khac
    

class LoginException(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    pass

async def login_exception_handler(request, exception:LoginException):
    return templates.TemplateResponse("login.html", context={"request": request, "check": "Tên tài khoản hoặc mật khẩu bạn nhập không chính xác."}, status_code=exception.status_code)


class UserNotPermissionException(Exception):
    status_code = status.HTTP_403_FORBIDDEN
    pass

async def user_not_permission_exception_handler(request, exception:UserNotPermissionException):
    return templates.TemplateResponse("login.html", context={"request": request, "check": "Permission Denied!"}, status_code=exception.status_code)
