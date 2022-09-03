import sys
sys.path.append(".")
from pydantic import BaseModel, constr, validator
from typing import Optional, Union, List
import string
import re
from datetime import datetime
from app.schemas.Role import Role

class UserBase(BaseModel):
    username:str
    token: str = None

class User(UserBase):
    id: int
    hashed_password: str
    role_id: int
    role: Role
    last_login: str
def validate_username(username)->str:
    if re.match(
        r"^(?=[a-zA-Z0-9._]{3,25}$)(?!.*[_.]{2})[^_.].*[^_.]$"
    , username):
        return username
    else:
        raise ValueError("Username invalid")

class UserCreate(UserBase):
    password: constr(min_length=3, max_length=10)
    @validator("username", pre=True)
    def username_is_valid(cls, username: str)->str:
        return validate_username(username=username)

class UserPublic(BaseModel):
    id: int
    username: str
    last_login: Union[str, None] = None
    role: str
    permission: str

if __name__  == "__main__":
    a = UserCreate(username="teca", password="123")
    
