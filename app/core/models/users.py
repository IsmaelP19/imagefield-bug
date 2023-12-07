from abc import abstractmethod
from typing import Any, Dict
from pydantic import validator
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, make_transient_to_detached
from starlette.requests import Request
from core.models.database import Base
import re
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin import ExportType

regexp = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    facilities = relationship("Facilities",
                              secondary="facilities_user_association",
                              back_populates="users"
                              )
    
    async def __admin_repr__(self, request):
        return f"{self.name} {self.last_name}"
    
    async def __admin_select2_repr__(self, request):
        return f'<span><span>#{(self.id)}</span> <strong>{(self.name)} {(self.last_name)}</strong> - {(self.email)}</span>'
        



class Users_View(ModelView):
    exclude_fields_from_list = ['password']
    fields = ['id', 'name', 'last_name', 'email', 'password', 'is_active', 'is_superuser', 'facilities']
    
    
    @abstractmethod
    async def create(self, request, data, *args,):
        await self.validate(request, data)
        user = await create_or_update_user(request, data, new=True)
        return user
    
    @abstractmethod
    async def edit(self, request, data, *args):
        sentData = args[0].copy()
        sentData['id'] = data
        await self.validate(request, sentData)
        user = await create_or_update_user(request, sentData)
        return user
    
    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        from ..services.database_service import get_user_by_email, get_user
        from dependencies import get_db

        db = next(get_db())

        errors: Dict[str, str] = {}
        if data["name"] is None or len(data["name"]) < 3:
            errors["name"] = "Introduce un nombre de al menos 3 caracteres"
        if data["last_name"] is None or len(data["last_name"]) < 3:
            errors["last_name"] = "Introduce un apellido de al menos 3 caracteres"
        if data["email"] is None or not re.fullmatch(regexp, data['email']):
            errors["email"] = "Introduce un email válido"

        if data.get('id') is None: # creating new user
            userEmail = get_user_by_email(db, data['email'])
            if userEmail:
                errors["email"] = "El email ya existe"

            if data["password"] is None or not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', data['password']):
                errors["password"] = "Introduce una contraseña válida (mínimo 8 caracteres, incluyendo letras, números y caracteres especiales)"

        else: # updating user
            user = get_user(db, data['id'])
            if user.email != data['email']: 
                userEmail = get_user_by_email(db, data['email'])
                if userEmail:
                    errors["email"] = "El email ya existe"

            if user.password != data['password']:
                if data["password"] is None or not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', data['password']):
                    errors["password"] = "Introduce una contraseña válida (mínimo 8 caracteres, incluyendo letras, números y caracteres especiales)"

        if len(errors) > 0:
            raise FormValidationError(errors)
        return await super().validate(request, data)

        


async def create_or_update_user(request, data, new=False): 
    from dependencies import get_db
    from .services import get_password_hash
    from ..services.database_service import get_user_by_email, get_user
    from core.models.facilities_crud import get_inst

    db = next(get_db())

    user_data = data.copy()

    password = user_data.pop('password', None)
    facilities = user_data.pop('facilities', None)
    
    if password is not None:
        if new: # create
            user = User(**user_data)
            user.password =  get_password_hash(password)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        else: 
            user =  get_user(db, data['id'])
            for key, value in user_data.items():
                setattr(user, key, value)  

            if (user.password != password): #to prevent hashing the already hashed password again
                user.password = get_password_hash(password)
            user.facilities = []
            db.commit()
            db.refresh(user)
        
        if facilities: # update user-facilities relationship
            for id in facilities:
                facility = get_inst(db, id)
                user.facilities.append(facility)
            db.commit()
            db.refresh(user)
        
        return user

    return None
