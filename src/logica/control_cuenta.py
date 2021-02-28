from sqlalchemy import func

from src.modelo.declarative_base import engine, Base, session
from src.modelo.actividad import Actividad, ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto


class ControlCuenta():

    def __init__(self):
        # TODO: Remover datos de prueba del Constructor a medida que se desarrollan las historias de usuario
        self.actividades = ["Actividad 1", "Actividad 2", "Actividad 3"]
        self.viajeros = [{"Nombre":"Pepe", "Apellido":"Pérez"}, {"Nombre":"Ana", "Apellido":"Andrade"}]
        self.gastos = [{"Concepto":"Gasto 1", "Fecha": "12-12-2020", "Valor": 10000, "Nombre": "Pepe", "Apellido": "Pérez"}, {"Concepto":"Gasto 2", "Fecha": "12-12-2020", "Valor": 20000, "Nombre":"Ana", "Apellido":"Andrade"}]
        self.matriz = [["", "Pepe Pérez", "Ana Andrade", "Pedro Navajas" ],["Pepe Pérez", -1, 1200, 1000],["Ana Andrade", 0, -1, 1000], ["Pedro Navajas", 0, 0, -1]]
        self.gastos_consolidados = [{"Nombre":"Pepe", "Apellido":"Pérez", "Valor":15000}, {"Nombre":"Ana", "Apellido":"Andrade", "Valor":12000},{"Nombre":"Pedro", "Apellido":"Navajas", "Valor":0}]
        self.viajeros_en_actividad = [{"Nombre": "Pepe Pérez", "Presente":True}, {"Nombre": "Ana Andrade", "Presente":True}, {"Nombre":"Pedro Navajas", "Presente":False}]
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
