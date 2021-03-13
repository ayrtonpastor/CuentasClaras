from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.modelo.declarative_base import engine, Base, session
from src.modelo.actividad import Actividad, ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto


class ControlCuenta():

    def __init__(self):
        # TODO: Remover datos de prueba del Constructor a medida que se desarrollan las historias de usuario
        Base.metadata.create_all(engine)

    def listarActividades(self):
        return session.query(Actividad).all()

    def crearReporteCompensacion(self, actividad_id):
        actividad_viajeros = session.query(
            ActividadViajero).filter_by(actividad_id=actividad_id)

        matriz = []
        cabecera = [" "]
        for actividad_viajero in actividad_viajeros:
            viajero = session.query(Viajero).filter_by(
                id=actividad_viajero.viajero_id).first()
            cabecera.append(viajero.nombre + ' ' + viajero.apellido)
        matriz.append(cabecera)

        query_monto_gastos_por_actividad = session.query(
            func.sum(Gasto.monto)).filter_by(actividad_id=actividad_id).first()
        monto_gastos_por_actividad = query_monto_gastos_por_actividad[
            0] if query_monto_gastos_por_actividad[0] else 0
        if monto_gastos_por_actividad == 0:
            return matriz

        promedio_gastos_viajero = monto_gastos_por_actividad/actividad_viajeros.count()

        cantidad_para_compensar = []
        for i in range(actividad_viajeros.count()):
            viajero_id = actividad_viajeros[i].viajero_id
            gastos_por_viajero = session.query(func.sum(Gasto.monto)).filter_by(
                actividad_id=actividad_id, viajero_id=viajero_id).first()
            monto_gasto_por_viajero = gastos_por_viajero[0] if gastos_por_viajero[0] else 0

            compensacion = monto_gasto_por_viajero - promedio_gastos_viajero
            cantidad_para_compensar.append(compensacion)

        for i in range(actividad_viajeros.count()):
            viajero_id = actividad_viajeros[i].viajero_id
            viajero = session.query(Viajero).filter_by(id=viajero_id).first()
            gastos_por_viajero = session.query(func.sum(Gasto.monto)).filter_by(
                actividad_id=actividad_id, viajero_id=viajero_id).first()
            monto_gasto_por_viajero = gastos_por_viajero[0] if gastos_por_viajero[0] else 0
            fila = [viajero.nombre + ' ' + viajero.apellido]
            cantidad_por_compensar = promedio_gastos_viajero - monto_gasto_por_viajero

            for j in range(len(cantidad_para_compensar)):
                if i == j:
                    fila.append(-1)
                else:
                    if cantidad_por_compensar <= 0 or cantidad_para_compensar[j] <= 0:
                        fila.append('0.00')
                    else:
                        if cantidad_por_compensar <= cantidad_para_compensar[j]:
                            fila.append("{:.2f}".format(
                                cantidad_por_compensar))
                            cantidad_para_compensar[j] -= cantidad_por_compensar
                            cantidad_por_compensar = 0
                        else:
                            fila.append("{:.2f}".format(
                                cantidad_para_compensar[j]))
                            cantidad_por_compensar -= cantidad_para_compensar[j]
                            cantidad_para_compensar[j] = 0

            matriz.append(fila)

        return matriz

    def crearReporteGastosPorViajero(self, actividad_id):
        actividad_viajeros = session.query(
            ActividadViajero).filter_by(actividad_id=actividad_id)
        matriz = []

        for actividad_viajero in actividad_viajeros:
            viajero = session.query(Viajero).filter_by(
                id=actividad_viajero.viajero_id).first()
            gastos_por_viajero = session.query(func.sum(Gasto.monto)).filter_by(
                actividad_id=actividad_id, viajero_id=viajero.id).first()
            monto_gasto_por_viajero = gastos_por_viajero[0] if gastos_por_viajero[0] else 0
            consolidado_viajero = {"Nombre": viajero.nombre, "Apellido": viajero.apellido,
                                   "Valor": "{:.2f}".format(monto_gasto_por_viajero)}
            matriz.append(consolidado_viajero)

        return matriz

    def crearReporteCompensacionproto(self, actividad_id):
        actividad_viajeros = session.query(
            ActividadViajero).filter_by(actividad_id=actividad_id)
        if actividad_viajeros.count() == 0:
            return []
        else:
            objetos = []
            for actividad_viajero in actividad_viajeros:
                gastos_por_viajero = session.query(func.sum(Gasto.monto)).filter_by(actividad_id=actividad_id,
                                                                                    viajero_id=actividad_viajero.viajero_id).first()
                monto_gasto_por_viajero = gastos_por_viajero[0] if gastos_por_viajero[0] else 0

                viajero = session.query(Viajero).filter_by(
                    id=actividad_viajero.viajero_id).first()
                promedio = monto_gasto_por_viajero / actividad_viajeros.count()

                objeto = {
                    "nombre": viajero.nombre + ' ' + viajero.apellido,
                    "monto_debe_cada_uno": "{:.2f}".format(promedio)
                }
                objetos.append(objeto)
        return objetos

    def listarGastos(self, actividad_id):
        actividad = session.query(Actividad).filter_by(id=actividad_id).first()
        return actividad.gastos

    def listarViajeros(self):
        return session.query(Viajero).all()

    def crearViajero(self, nombre, apellido):
        if nombre is None or nombre == "" or apellido is None or apellido == "":
            return False
        else:
            nombre = nombre.strip()
            apellido = apellido.strip()
            viajeros = session.query(Viajero).filter(
                Viajero.nombre == nombre, Viajero.apellido == apellido).all()
            if len(viajeros) == 0:
                viajero = Viajero(nombre=nombre, apellido=apellido)
                session.add(viajero)
                session.commit()
                return True
            else:
                return False

    def editarViajero(self, viajero_id, nvo_nombre, nvo_apellido):
        if nvo_nombre is None or nvo_nombre == "" or nvo_apellido is None or nvo_apellido == "":
            return False
        else:
            viajero = session.query(Viajero).filter_by(id=viajero_id).first()

            if viajero:
                nvo_nombre = nvo_nombre.strip()
                nvo_apellido = nvo_apellido.strip()
                viajeros = session.query(Viajero).filter(
                    Viajero.nombre == nvo_nombre, Viajero.apellido == nvo_apellido, Viajero.id != viajero_id).all()
                if len(viajeros) == 0:
                    viajero.nombre = nvo_nombre
                    viajero.apellido = nvo_apellido
                    session.commit()
                    return True
                else:
                    return False
            else:
                return False

    def crearActividad(self, nombre):
        if not nombre:
            return None
        try:
            _actividad = Actividad(nombre=nombre, terminada=False)
            session.add(_actividad)
            session.commit()
            return _actividad
        except IntegrityError as exception:
            session.rollback()
            raise exception

    def asociarViajeroAActividad(self, actividad_id, viajero_id):
        if not actividad_id or not viajero_id:
            return None
        try:
            _actividad_viajero = ActividadViajero(
                actividad_id=actividad_id, viajero_id=viajero_id)
            session.add(_actividad_viajero)
            session.commit()
            return _actividad_viajero
        except IntegrityError as exception:
            session.rollback()
            raise exception

    def eliminarActividadViajero(self, actividad_id, viajero_id):
        # TODO: verificar constraints, si la actividad esta terminada, o si hay gastos
        if not actividad_id or not viajero_id:
            return None
        try:

            if session.query(Gasto).filter(Gasto.viajero_id == viajero_id, Gasto.actividad_id == actividad_id).count() > 0:
                raise Exception("No se puede eliminar viajero con gastos")

            m_actividad = session.query(Actividad).filter(
                Actividad.id == actividad_id).first()
            if m_actividad.terminada:
                raise Exception(
                    "No se puede eliminar viajero de una actividad terminada")

            _actividad_viajero = session.query(ActividadViajero).filter(
                ActividadViajero.actividad_id == actividad_id,
                ActividadViajero.viajero_id == viajero_id
            ).first()
            session.delete(_actividad_viajero)
            session.commit()

        except IntegrityError as exception:
            session.rollback()
            raise exception

    def darListaViajerosActividad(self, actividad_id):
        return session.query(ActividadViajero).filter(ActividadViajero.actividad_id == actividad_id)
    
    def eliminarActividad(self, actividad_id):
        if not actividad_id:
            return None

        try:
            m_actividad = session.query(Actividad).filter(Actividad.id == actividad_id).first()

            if len(m_actividad.gastos) > 0:
                raise Exception(
                        "No se puede eliminar una actividad que contiene gastos")
            
            if m_actividad.terminada:
                    raise Exception(
                        "No se puede eliminar una actividad que está terminada")
            
            session.delete(m_actividad)
            session.commit()
            
        except IntegrityError as exception:
            session.rollback()
            raise exception
