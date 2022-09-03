from pydantic import BaseModel, constr, validator
from typing import Optional, Union, List
import string
import re
###### class Base ######
class UserBase(BaseModel):
    username:str
    token: str = None

class PermissionBase(BaseModel):
    permission: int
    description: str = None

class RoleBase(BaseModel):
    role: str
    description: str = None

###### class parent ######


class Permission(PermissionBase):
    id: int
 
class RolePermission(BaseModel):
    role_id: int
    permission_id: int
    permission: List[Permission]

class Role(RoleBase):
    id: int
    role_permission: RolePermission

class User(UserBase):
    id: int
    hashed_password: str
    role_id: int
    role: Role
    

# class PermissionDB(Permission):
#     class Config:
#         orm_mode = True

# class RoleDB(Role):
#     class Config:
#         orm_mode = True

# class RolePermissionDB(RolePermission):
#     class Config:
#         orm_mode = True

# class UserDB(User):
#     role_id: int
#     class Config:
#         orm_mode = True

### class create ###
class UserCreate(UserBase):
    password: str

# class RoleCreate(Role):
#     pass

# class PermissionCreate(Permission):
#     pass

# class RolePermissionCreate(RolePermission):
#     pass


### class ###
class RoleHasPermission(RoleBase):
    permissions: List[PermissionBase] = []

class UserPrivate(UserBase):
    role: RoleHasPermission
class userPublic(UserBase):
    pass
if __name__ == "__main__":
    # b = Permission(id=1, permission=7)
    # a = Role(id=1, role="admin", permission=[b])
    # u = UserCreate(id=1, username="nam", token="123", hashed_password="123",
    # role=a)
    pass
    