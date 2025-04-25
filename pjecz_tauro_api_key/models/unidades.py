"""
Unidades, modelos
"""

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Unidad(Base, UniversalMixin):
    """Unidad"""

    # Nombre de la tabla
    __tablename__ = "unidades"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    clave: Mapped[str] = mapped_column(String(16), unique=True)
    nombre: Mapped[str] = mapped_column(String(256))

    # Hijos
    ventanillas: Mapped[List["Ventanilla"]] = relationship(back_populates="unidad")

    def __repr__(self):
        """Representación"""
        return f"<Unidad {self.clave}>"
