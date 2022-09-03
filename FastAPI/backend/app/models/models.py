import sys
sys.path.append(".")
from enum import unique
from sqlalchemy import String, Column, ForeignKey, Integer, SmallInteger, PrimaryKeyConstraint, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable = False)
    username = Column(String(25), unique=True, index = True, nullable = False)
    hashed_password = Column(String(255), nullable = False)
    token = Column(String(255), nullable = True)
    last_login = Column(DateTime(), nullable = True)
    role = relationship("Role", back_populates="user")

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    role = Column(String(25), nullable = False)
    is_admin = Column(Boolean, nullable = False)
    description = Column(String(255), nullable = True)
    user = relationship("User", back_populates="role")
    role_permission = relationship("RolePermission", back_populates="role")

class Permission(Base):
    __tablename__ = "permission"
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    permission = Column(SmallInteger, nullable = False)
    description = Column(String(255), nullable = True)
    role_permission = relationship("RolePermission", back_populates="permission")

class RolePermission(Base):
    __tablename__ = "role_permission"
    role_id = Column(Integer, ForeignKey("role.id"), nullable = False)
    permission_id = Column(Integer, ForeignKey("permission.id"), nullable = False)
    __table_args__ = (
        PrimaryKeyConstraint(role_id, permission_id),
        {},
    )
    role = relationship("Role", back_populates="role_permission")
    permission = relationship("Permission", back_populates="role_permission")

# alembic init alembic -- sua file duong dan mysql, import vao file env.py tu model ==> Base
# alembic revision --autogenerate -m "First revision" -- tao code auto
# alembic upgrade "ten file" -- chay file auto  --> check trong database
# alembic downgrade -1 -- tro ve file auto dau tien

