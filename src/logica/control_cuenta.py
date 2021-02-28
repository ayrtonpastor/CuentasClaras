from src.modelo.declarative_base import engine, Base, session
from src.modelo.actividad import Actividad, ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto


class ControlCuenta():

    def __init__(self):
        Base.metadata.create_all(engine)

    def listarActividades(self):
        return session.query(Actividad).all()

    def crearReporteCompensacion(self, actividad_id):
        viajeros = session.query(ActividadViajero).filter_by(actividad_id=actividad_id)
        if viajeros.count() == 0:
            return []

    def listarGastos(self, actividad_id):
        actividad = session.query(Actividad).filter_by(id=actividad_id).first()
        return actividad.gastos
