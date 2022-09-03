import sys
sys.path.append(".")
from fastapi import Depends, HTTPException, status
from fastapi_login import LoginManager
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from app.database.database import DBContext, SessionLocal
from app.database import crud
from app.schemas import User
import app.database.password as pwd
from app.frontend import templates
from app.exceptions import exceptions
from fastapi import Request, Response
import jwt
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY_64')
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24
ALGORITHM = "HS256"

def get_database():
	with DBContext() as db:
		yield db

scopes = {"admin": "super user"}
manager = LoginManager(
    secret=SECRET_KEY,
    token_url="/login",
    scopes=scopes,
    cookie_name="auth",
    use_cookie=True,
    algorithm=ALGORITHM
)

@manager.user_loader()
def get_user(username: str, db: Session = None):
    if db is None:
        with DBContext() as db:
            return crud.get_user_by_username(db=db,username=username)
    return crud.get_user_by_username(db=db,username=username)

def authenticate_user(username: str, password: str, db: Session = Depends(get_database)):
    user:User.User = crud.get_user_by_username(db=db,username=username)
    if not user:
        return None
    if not pwd.verify_password(plain_password = password, hashed_password = user.hashed_password):
        return None
    return user

def payload_token( token, manager: LoginManager = manager):
    try:
        payload = jwt.decode(
            token, manager.secret.secret_for_decode, algorithms=[manager.algorithm]
        )
        return payload
    # This includes all errors raised by pyjwt
    except jwt.PyJWTError:
        raise manager.not_authenticated_exception

ROLE = {
    "GET" : 0, #1
    "POST": 1, #2
    "PUT" : 2, #4
    "DELETE" : 3 #8
}

def validate_token_role(request: Request, user: User.User = Depends(manager)):
    token = request.cookies.get(manager.cookie_name)
    if user.token == token:
        a = payload_token(token=token)
        get_bin:str = lambda x: format(x, 'b').zfill(4)
        binary_role:str = get_bin(a["permission"])[::-1]
        index = ROLE[request.method]
        if int(binary_role[index]):
            return user
        else:
            raise exceptions.UserNotPermissionException
    else:
        return exceptions.UserNotPermissionException



manager.not_authenticated_exception = exceptions.NotAuthenticatedException
# app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)