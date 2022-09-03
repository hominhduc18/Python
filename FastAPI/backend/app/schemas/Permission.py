from pydantic import BaseModel, constr, validator
from typing import Optional, Union, List
import string
import re

class PermissionBase(BaseModel):
    permission: int
    description: str = None

class Permission(PermissionBase):
    id: int