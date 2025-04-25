"""
Unidades, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.unidades import Unidad
from ..models.permisos import Permiso
from ..schemas.unidades import UnidadOut, OneUnidadOut

unidades = APIRouter(prefix="/api/v5/unidades", tags=["unidades"])


@unidades.get("/{clave}", response_model=OneUnidadOut)
async def detalle_unidades(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una unidad a partir de su clave"""
    if current_user.permissions.get("UNIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        unidad = database.query(Unidad).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneUnidadOut(success=False, message="No existe esa unidad", errors=[str(error)])
    if unidad.estatus != "A":
        message = "No está habilitada esa unidad"
        return OneUnidadOut(success=False, message=message, errors=[message])
    return OneUnidadOut(success=True, message=f"Detalle de {clave}", data=UnidadOut.model_validate(unidad))


@unidades.get("", response_model=CustomPage[UnidadOut])
async def paginado_unidades(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de unidades"""
    if current_user.permissions.get("UNIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Unidad).filter_by(estatus="A").order_by(Unidad.id.desc()))
