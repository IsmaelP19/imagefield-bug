from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
from sqlalchemy.orm import sessionmaker
import os

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")


SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/exampledb"

Base = declarative_base()



os.makedirs("./media/inst_pictures", exist_ok=True)
container = LocalStorageDriver("./media").get_container("inst_pictures")
StorageManager.add_storage("media", container)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)