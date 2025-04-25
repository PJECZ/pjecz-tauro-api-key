"""
Ventanillas, modelos
"""

from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Ventanilla(Base, UniversalMixin):
    """Ventanilla"""

    # Nombre de la tabla
    __tablename__ = "ventanillas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship(back_populates="ventanillas")
    unidad_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"))
    unidad: Mapped["Unidad"] = relationship(back_populates="ventanillas")

    # Columnas
    clave: Mapped[str] = mapped_column(String(16), unique=True)
    es_habilitada: Mapped[bool] = mapped_column(default=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(256))

    # Hijos
    turnos: Mapped[List["Turno"]] = relationship(back_populates="ventanilla")

    @property
    def usuario_email(self):
        """Email del usuario"""
        return self.usuario.email

    @property
    def unidad_clave(self):
        """Clave de la unidad"""
        return self.unidad.clave

    def __repr__(self):
        """Representación"""
        return f"<Ventanilla {self.id}>"
