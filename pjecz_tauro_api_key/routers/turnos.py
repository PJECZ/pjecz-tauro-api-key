"""
Turnos, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.turnos import Turno
from ..models.permisos import Permiso
from ..schemas.turnos import TurnoOut, OneTurnoOut

turnos = APIRouter(prefix="/api/v5/turnos", tags=["turnos"])


@turnos.get("/{turno_id}", response_model=OneTurnoOut)
async def detalle_turnos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    turno_id: int,
):
    """Detalle de un turno a partir de su ID"""
    if current_user.permissions.get("TURNOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    turno = database.query(Turno).get(turno_id)
    if not turno:
        message = "No existe ese turno"
        return OneTurnoOut(success=False, message=message, errors=[message])
    if turno.estatus != "A":
        message = "No está habilitado ese turno"
        return OneTurnoOut(success=False, message=message, errors=[message])
    return OneTurnoOut(success=True, message=f"Detalle de {turno_id}", data=TurnoOut.model_validate(turno))


@turnos.get("", response_model=CustomPage[TurnoOut])
async def paginado_turnos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de turnos"""
    if current_user.permissions.get("TURNOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Turno).filter_by(estatus="A").order_by(Turno.id.desc()))
