"""
Turnos, modelos
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Turno(Base, UniversalMixin):
    """Turno"""

    ESTADOS = {
        "EN_ESPERA": "En Espera",
        "ATENDIENDO": "Atendiendo",
        "COMPLETADO": "Completado",
    }

    TIPOS = {
        "NORMAL": "Normal",
        "CON_CITA": "Con Cita",
        "DISCAPACIDAD": "Discapacidad",
        "URGENTE": "Urgente",
    }

    # Nombre de la tabla
    __tablename__ = "turnos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship(back_populates="turnos")
    ventanilla_id: Mapped[int] = mapped_column(ForeignKey("ventanillas.id"))
    ventanilla: Mapped["Ventanilla"] = relationship(back_populates="turnos")

    # Columnas
    numero: Mapped[int]
    clave: Mapped[str] = mapped_column(String(16))
    # turno_solicitado: Mapped[str] = mapped_column(String(512))  # Es el ID del sistema externo que hace la petición de creación de un nuevo turno
    tipo: Mapped[str] = mapped_column(Enum(*TIPOS, name="turnos_tipos", native_enum=False), index=True)
    inicio: Mapped[datetime] = mapped_column(DateTime, default=now())
    termino: Mapped[datetime] = mapped_column(DateTime, default=now())
    estado: Mapped[str] = mapped_column(Enum(*ESTADOS, name="turnos_estados", native_enum=False), index=True)
    comentarios: Mapped[Optional[str]] = mapped_column(String(512))

    @property
    def usuario_email(self):
        """Email del usuario"""
        return self.usuario.email

    @property
    def ventanilla_clave(self):
        """Clave de la ventanilla"""
        return self.ventanilla.clave

    def __repr__(self):
        """Representación"""
        return f"<Turno {self.id}>"
