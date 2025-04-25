"""
Unidades, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class UnidadOut(BaseModel):
    """Esquema para entregar unidades"""

    id: int
    clave: str
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneUnidadOut(OneBaseOut):
    """Esquema para entregar una unidad"""

    data: UnidadOut | None = None
