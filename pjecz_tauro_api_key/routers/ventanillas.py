"""
Ventanillas, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.ventanillas import Ventanilla
from ..models.permisos import Permiso
from ..schemas.ventanillas import VentanillaOut, OneVentanillaOut

ventanillas = APIRouter(prefix="/api/v5/ventanillas", tags=["ventanillas"])


@ventanillas.get("/{clave}", response_model=OneVentanillaOut)
async def detalle_ventanillas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una ventanilla a partir de su clave"""
    if current_user.permissions.get("VENTANILLAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        ventanilla = database.query(Ventanilla).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneVentanillaOut(success=False, message="No existe esa ventanilla", errors=[str(error)])
    if ventanilla.estatus != "A":
        message = "No está habilitada esa ventanilla"
        return OneVentanillaOut(success=False, message=message, errors=[message])
    return OneVentanillaOut(success=True, message=f"Detalle de {clave}", data=VentanillaOut.model_validate(ventanilla))


@ventanillas.get("", response_model=CustomPage[VentanillaOut])
async def paginado_ventanillas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de ventanillas"""
    if current_user.permissions.get("VENTANILLAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Ventanilla).filter_by(estatus="A").order_by(Ventanilla.clave))
