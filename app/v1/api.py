from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from v1.endpoints.insts import router_insts
from core.models.database import engine

from starlette_admin.contrib.sqla import Admin
from core.models.facilities import Facilities as Insts, Insts_View
from starlette.middleware.sessions import SessionMiddleware


# Esquema de seguridad HTTPBasic
security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="!secret")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Example Data",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema



admin = Admin(engine, title="Administrador", base_url="/admin")

app.include_router(router_insts)

admin.add_view(Insts_View(Insts, icon='fa fa-cog', label='Instalaciones'))



admin.mount_to(app)