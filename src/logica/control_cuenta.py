from src.modelo.declarative_base import engine, Base, session
from src.modelo.actividad import Actividad


class ControlCuenta():

    def __init__(self):
        Base.metadata.create_all(engine)

    def listarActividades(self):
        return session.query(Actividad).all()

    def crearReporteCompensacion(self, actividad_id):
        pass

    def listarGastos(self, actividad_id):
        pass
