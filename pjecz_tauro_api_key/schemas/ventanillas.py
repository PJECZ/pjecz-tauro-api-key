"""
Ventanillas, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class VentanillaOut(BaseModel):
    """Esquema para entregar ventanillas"""

    id: int
    usuario_email: str
    unidad_clave: str
    clave: str
    es_habilitada: bool
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneVentanillaOut(OneBaseOut):
    """Esquema para entregar una ventanilla"""

    data: VentanillaOut | None = None
