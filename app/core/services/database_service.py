# from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session
from ..models import users
from ..schemas import schemas
 
# from models import User
# from ..schemas import UserCreate


def get_user(db: Session, user_id: int):
    res = db.query(users.User).filter(users.User.id == user_id).first()
    return db.query(users.User).filter(users.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(users.User).filter(users.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(users.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    from .services import get_password_hash

    values = user.dict()
    password = values.pop('password', None)
    if password is not None:
        user = users.User(**values)
        user.password = get_password_hash(password)
        db.add(user)
        db.commit()
        return user
    return None

