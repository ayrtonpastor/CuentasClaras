from sqlalchemy import Column, Integer, String
from .declarative_base import Base


class Viajero(Base):
    __tablename__ = 'viajero'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
