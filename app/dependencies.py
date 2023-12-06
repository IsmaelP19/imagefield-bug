import configparser
from core.models.database import SessionLocal
from fastapi import Depends

config = configparser.RawConfigParser()
config.read('app/config.properties')

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()