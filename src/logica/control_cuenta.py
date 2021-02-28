from sqlalchemy import func

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
        actividad_viajeros = session.query(ActividadViajero).filter_by(actividad_id=actividad_id)
        if actividad_viajeros.count() == 0:
            return []
        else:
            objetos = []
            for actividad_viajero in actividad_viajeros:
                gastos_por_viajero = session.query(func.sum(Gasto.monto)).filter_by(actividad_id=actividad_id,
                                                                                    viajero_id=actividad_viajero.viajero_id).first()
                monto_gasto_por_viajero = gastos_por_viajero[0] if gastos_por_viajero[0] else 0

                viajero = session.query(Viajero).filter_by(id=actividad_viajero.viajero_id).first()
                promedio = monto_gasto_por_viajero / actividad_viajeros.count()

                objeto = {
                    "nombre": viajero.nombre + ' ' + viajero.apellido,
                    "monto_debe_cada_uno": "{:.2f}".format(promedio)
                }
                objetos.append(objeto)
        print(objetos)
        return objetos

    def listarGastos(self, actividad_id):
        actividad = session.query(Actividad).filter_by(id=actividad_id).first()
        return actividad.gastos
