import sys
from datetime import datetime
sys.path.append(".")
from sqlalchemy.orm import Session
from app.database import database
from app.models import models
from app.schemas import User, Role, RolePermission, Permission
import app.database.password as pwd

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(
        models.User.id == id).first()

def get_all_user(db: Session):
    return db.query(models.User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username).first()

def update_user_token(db: Session, username: str, token: str):
    user = get_user_by_username(db=db, username=username)
    user.token = token
    db.commit()

def update_user_password(db: Session, username: str, new_password: str, old_password: str):
    user:User.User = get_user_by_username(db=db, username=username)
    if pwd.verify_password(old_password, user.hashed_password):
        user.hashed_password = pwd.get_hashed_password(new_password)
        db.commit()
        return user
    return None

def get_role_by_id(db: Session, id: id):
    return db.query(models.Role).filter(
        models.Role.id == id).first()

def get_role_user_join(db: Session, user_id: int):
    return db.query(models.User).join(models.Role).join(models.RolePermission).join(models.Permission).filter(models.Role.id == user_id).first()

def get_last_id(db:Session)-> int:
    try:
        return db.query(models.User).order_by(models.User.id.desc()).first().id+1
    except:
        return 1

def create_user(db: Session, user: User.UserCreate, role: int):
    role_id = get_role_by_id(db=db, id = role)
    if role_id == None:
        print("Role not exist")
        return None
    user_id = get_last_id(db=db)
    user_role = role
    db_user = models.User(
        id = user_id,
        role_id = user_role,
        username = user.username,
        hashed_password = pwd.get_hashed_password(user.password),
        token = user.token
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        print("Username already exist")
        return None

if __name__ == "__main__":
    with database.DBContext() as db:
        
        # a = get_role_user_join(db=db, user_id = 1)
        # b = get_user(db=db, id = 1)
        
        # for i in b.role.role_permission:
        #     print(i.permission.permission)
        # print(a.role.role_permission[2].permission.permission)
        for i in range(5):
            user = User.UserCreate(username=f"guest{i+1}", password="123")
            a = create_user(db=db, user = user, role=3)

        # user:User.User = get_user_by_username(db = db, username="test")
        # print(user.role.role_permission[0].permission.permission)
        # # user_role = schemas.RoleHasPermission(role = user.role.role, description=user.role.description)
        # permisssions = list()
        # for i in user.role.role_permission:
        #     print(i.permission.permission)
            # permission = Permission.PermissionBase(permission=i.permission.permission, description=i.permission.description)
            # permisssions.append(permission)
        # user_role.permissions = permisssions
        # user = schemas.UserPrivate(username=user.username, token=user.token, role = user_role)
        # print(user)
        # update_user_token(db, "teca", "dkssssm")
        # update_user_password(db=db, username="teca", new_password="1234", old_password="123")
        # lst = get_all_user(db)
        # print(lst[0].)
        # user:User.User = get_user_by_username(db=db, username="test")
        # # user.last_login = datetime.now()
        # # db.commit()
        
        # date_string = f'{datetime.now():%d-%m-%Y %H:%M:%S%z}'
        # user.last_login = f'{datetime.now():%d-%m-%Y %H:%M:%S%z}'
        # db.commit()
        pass
