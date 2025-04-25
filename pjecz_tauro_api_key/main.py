"""
PJECZ Tauro API Key
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from .routers.autoridades import autoridades
from .routers.distritos import distritos
from .routers.modulos import modulos
from .routers.permisos import permisos
from .routers.roles import roles
from .routers.turnos import turnos
from .routers.unidades import unidades
from .routers.usuarios import usuarios
from .routers.usuarios_roles import usuarios_roles
from .routers.ventanillas import ventanillas
from .settings import get_settings

# FastAPI
app = FastAPI(
    title="PJECZ API del Sistema de Turnos",
    description="",
    docs_url="/docs",
    redoc_url=None,
)

# CORSMiddleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins.split(","),
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Rutas
app.include_router(autoridades, include_in_schema=False)
app.include_router(distritos, include_in_schema=False)
app.include_router(modulos, include_in_schema=False)
app.include_router(permisos, include_in_schema=False)
app.include_router(roles, include_in_schema=False)
app.include_router(turnos)
app.include_router(unidades)
app.include_router(usuarios, include_in_schema=False)
app.include_router(usuarios_roles, include_in_schema=False)
app.include_router(ventanillas)

# Paginación
add_pagination(app)


# Mensaje de Bienvenida
@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Bienvenido a la API del Sistema de Turnos."}
