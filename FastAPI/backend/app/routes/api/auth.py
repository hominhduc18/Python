from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException,Request, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.frontend import templates
from app.routes import login_manager
from app.models import models
from app.schemas import User
from app.database import crud
from app.database import password as pwd
from app.exceptions import exceptions
from datetime import datetime
router = APIRouter()

@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse(name = "login.html", context={"request": request, "title": "Login"})
    return response

@router.post('/login', response_class=RedirectResponse)
async def post_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(login_manager.get_database)):
    user:User.User = login_manager.authenticate_user(username=form_data.username, password = form_data.password, db = db)
    if not user:
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Incorrect username or password",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        raise exceptions.LoginException
    user.last_login = datetime.now()
    db.commit()
    permission = 0
    for i in user.role.role_permission:
        permission += i.permission.permission
    
    scopes = []
    if user.role.role in login_manager.scopes:
        scopes.append(user.role.role)

    access_token_expires = timedelta(minutes=login_manager.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = login_manager.manager.create_access_token(
        data={"sub": user.username, "scopes": scopes, "permission": permission},
        expires=access_token_expires
        )
    crud.update_user_token(db=db, username=user.username, token=access_token)
    resp = RedirectResponse("/dashboard", status_code=status.HTTP_302_FOUND)
    login_manager.manager.set_cookie(resp,access_token)
    return resp

@router.get('/logout')
async def logout(user:User.User=Depends(login_manager.manager), db: Session = Depends(login_manager.get_database)):
    resp = RedirectResponse("/login")
    resp.delete_cookie(key=login_manager.manager.cookie_name)
    crud.update_user_token(db=db, username=user.username, token="")
    return resp

@router.get("/change-password")
async def get_change_password(request: Request, user:User.User=Depends(login_manager.manager)):
    return templates.TemplateResponse("changePassWord.html", {"request": request, "title": "Change Password"})

@router.post("/change-password")
async def post_change_password(request: Request,db: Session = Depends(login_manager.get_database), password_old = Form(...), password_new = Form(...), user: User.User = Depends(login_manager.manager)):
    rs = crud.update_user_password(db=db, username=user.username, new_password = password_new, old_password = password_old)
    if rs:
        resp = RedirectResponse("/dashboard", status_code=status.HTTP_302_FOUND) # 307 vong lap vo han post
    else:
        resp = templates.TemplateResponse("changePassWord.html", {"request": request, "title": "Change Password", "check": "Mật khẩu bạn nhập không chính xác"}, status_code=status.HTTP_403_FORBIDDEN)
    return resp
     

# @router.post("/test")
# async def test(request: Request, user: User.User = Depends(login_manager.validate_token_role)):
#     print(user)
#     return {"haha": "hahaa"}

# @router.get("/tt")
# async def tt(request: Request):
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)