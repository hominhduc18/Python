from pydantic import BaseModel, constr, validator
from typing import Optional, Union, List
import string
import re
from app.schemas.Permission import Permission

class RolePermission(BaseModel):
    role_id: int
    permission_id: int
    permission: Permission