from pydantic import BaseModel, constr, validator
from typing import Optional, Union, List
import string
import re
from app.schemas.RolePermission import RolePermission

class RoleBase(BaseModel):
    role: str
    description: str = None

class Role(RoleBase):
    id: int
    role_permission: List[RolePermission]