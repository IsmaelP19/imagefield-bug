from pydantic import BaseModel
from typing import Optional
from typing import List

class UserBase(BaseModel):
    name: str
    last_name: str
    email: str

class InstBase(BaseModel):
    ins_fea_name: str
    ins_fea_desc: Optional[str] = None
    ins_fea_img: Optional[str] = None
    users: List[UserBase] = None
 
    class Config:
        from_attributes = True


class InstCreate(InstBase):
    ins_fea_id: int


class UserCreate(UserBase):
    password: str
    is_active: bool
    is_superuser: bool

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserInformation(User):
    is_superuser: bool
    facilities: List[InstCreate]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    uid: int