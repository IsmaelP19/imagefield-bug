from datetime import timedelta

from typing import Annotated
from fastapi import Depends, Form, HTTPException, status, APIRouter, Body
from sqlalchemy.orm import Session

from core.schemas.schemas import User, Token, UserCreate, UserLogin, UserInformation

from core.services.services import authenticate_user, create_access_token
from dependencies import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_db
from core.services.database_service import create_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=UserInformation)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/token", response_model=Token)
# async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], db: Annotated[Session, Depends(get_db)]):
async def login(user_data: UserLogin = Body(...), db: Session = Depends(get_db)):
    email = user_data.email
    password = user_data.password

    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "uid": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=User)
async def signup(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_user = authenticate_user(db, user.email, user.password)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)