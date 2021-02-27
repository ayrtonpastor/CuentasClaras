from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .declarative_base import Base
from sqlalchemy.orm import relationship


class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    terminada = Column(Boolean)

    gastos = relationship('Gasto', backref='gasto',
                          cascade='all, delete, delete-orphan')
    viajeros = relationship('Viajero', secondary='actividad_viajero')


class ActividadViajero(Base):
    __tablename__ = 'actividad_viajero'

    actividad_id = Column(Integer, ForeignKey(
        'actividad.id'), primary_key=True)
    viajero_id = Column(Integer, ForeignKey('viajero.id'), primary_key=True)
