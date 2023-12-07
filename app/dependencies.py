import configparser

from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


from core.models.database import SessionLocal
from core.services.database_service import get_user

config = configparser.RawConfigParser()
config.read('app/config.properties')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = config.get('Credentials', 'SECRET_KEY')
ALGORITHM = config.get('Credentials', 'ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get('Credentials', 'ACCESS_TOKEN_EXPIRE_MINUTES'))


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: int = payload.get("uid")
        if uid is None:
            raise credentials_exception
        user = get_user(db, user_id=uid)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

