from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship
from .declarative_base import Base


class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column(Integer, primary_key=True)
    concepto = Column(String)
    monto = Column(Numeric(precision=2))
    fecha = Column(Date)

    viajero = relationship("Viajero", backref="gasto")
    actividad = relationship("Actividad", back_populates="gastos")

    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    viajero_id = Column(Integer, ForeignKey('viajero.id'), nullable=False)
