from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from .services import authenticate_user
from dependencies import get_db
from .database_service import get_user_by_email

class CustomProvider(AuthProvider):
  async def login(self, email: str, password: str, remember_me: bool, request: Request, response: Response) -> Response:

    db = next(get_db())
    user = authenticate_user(db, email, password)
    if not user:
      raise LoginFailed("Correo electrónico o contraseña incorrectos")
    if not user.is_superuser:
      raise LoginFailed('Introduce las credenciales de un administrador')
    response.set_cookie("user", user.email)
    request.session.update({"email": email})
    return response
  
  async def is_authenticated(self, request: Request) -> bool:
    email = request.session.get("email")
    if not email:
      return False
    db = next(get_db())
    user = get_user_by_email(db, email)
    if not user or not user.is_superuser:
      return False
    
    return True  
  
  async def logout(self, request: Request, response: Response) -> Response:
    response.delete_cookie("user")
    request.session.pop("email", None)
    return response
