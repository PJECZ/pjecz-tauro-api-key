"""
Turnos, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class TurnoOut(BaseModel):
    """Esquema para entregar turnos"""

    id: int
    usuario_email: str
    ventanilla_clave: str
    numero: int
    clave: str
    tipo: str
    inicio: datetime
    termino: datetime
    estado: str
    comentarios: str
    model_config = ConfigDict(from_attributes=True)


class OneTurnoOut(OneBaseOut):
    """Esquema para entregar un turno"""

    data: TurnoOut | None = None
