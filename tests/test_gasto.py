import random
import unittest

from faker import Faker
from src.logica.control_cuenta import ControlCuenta
from src.modelo.actividad import Actividad, ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.declarative_base import Session
from datetime import date


class ActividadTestCase(unittest.TestCase):
    def setUp(self):
        self.control_cuenta = ControlCuenta()
        self.session = Session()
        """ Generación de datos aleatorios """
        self.data_factory = Faker()

        self.actividad1 = Actividad(nombre=self.data_factory.word(), terminada=False)
        self.actividad2 = Actividad(nombre=self.data_factory.word(), terminada=False)
        self.actividad3 = Actividad(nombre=self.data_factory.word(), terminada=False)
        self.actividad4 = Actividad(nombre=self.data_factory.word(), terminada=True)

        self.session.add_all([self.actividad1, self.actividad2, self.actividad3, self.actividad4])

        self.viajero1 = Viajero(nombre=self.data_factory.name(), apellido=self.data_factory.name())
        self.viajero2 = Viajero(nombre=self.data_factory.name(), apellido=self.data_factory.name())
        self.viajero3 = Viajero(nombre=self.data_factory.name(), apellido=self.data_factory.name())
        self.viajero4 = Viajero(nombre=self.data_factory.name(), apellido=self.data_factory.name())

        self.session.add_all([self.viajero1, self.viajero2, self.viajero3, self.viajero4])
        self.session.flush()

        # Viajeros asociados a actividad 1
        self.actividad_viajero1 = ActividadViajero(actividad_id=self.actividad1.id, viajero_id=self.viajero1.id)
        self.actividad_viajero2 = ActividadViajero(actividad_id=self.actividad1.id, viajero_id=self.viajero2.id)

        # Viajeros asociados a actividad 2
        self.actividad_viajero3 = ActividadViajero(actividad_id=self.actividad2.id, viajero_id=self.viajero3.id)
        self.actividad_viajero4 = ActividadViajero(actividad_id=self.actividad2.id, viajero_id=self.viajero4.id)

        # Viajeros asociados a actividad 4
        self.actividad_viajero5 = ActividadViajero(actividad_id=self.actividad4.id, viajero_id=self.viajero1.id)

        self.session.add_all([self.actividad_viajero1, self.actividad_viajero2, self.actividad_viajero3,
                              self.actividad_viajero4, self.actividad_viajero5])

        # Gastos asociados a la actividad 1
        self.gasto1 = self.gasto_aleatorio(self.actividad1.id, self.viajero1.id)
        self.gasto2 = self.gasto_aleatorio(self.actividad1.id, self.viajero2.id)

        # Gastos asociados a la actividad 2
        self.gasto3 = self.gasto_aleatorio(self.actividad2.id, self.viajero3.id)

        # Gastos asociados a la actividad 4
        self.gasto4 = self.gasto_aleatorio(self.actividad4.id, self.viajero1.id)

        self.session.add_all([self.gasto1, self.gasto2, self.gasto3, self.gasto4])

        self.session.commit()

        self.gasto1_id = self.gasto1.id
        self.gasto3_id = self.gasto3.id
        self.gasto4_id = self.gasto4.id

        self.gasto1_concepto = self.gasto1.concepto
        self.gasto2_concepto = self.gasto2.concepto
        self.gasto3_concepto = self.gasto3.concepto

        self.actividad1_id = self.actividad1.id
        self.actividad2_id = self.actividad2.id
        self.actividad3_id = self.actividad3.id

        self.viajero1_id = self.viajero1.id
        self.viajero2_id = self.viajero2.id
        self.viajero3_id = self.viajero3.id
        self.viajero4_id = self.viajero4.id

        self.session.close()

    def tearDown(self):
        self.session = Session()

        gastos = self.session.query(Gasto).all()
        actividad_viajeros = self.session.query(ActividadViajero).all()
        actividades = self.session.query(Actividad).all()
        viajeros = self.session.query(Viajero).all()

        for gasto in gastos:
            self.session.delete(gasto)

        for actividad_viajero in actividad_viajeros:
            self.session.delete(actividad_viajero)

        for actividad in actividades:
            self.session.delete(actividad)

        for viajero in viajeros:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()

    def test_listar_gastos(self):
        # conteo de cantidades de gastos por actividad
        gastos_actividad1 = self.control_cuenta.listarGastos(self.actividad1_id)
        gastos_actividad2 = self.control_cuenta.listarGastos(self.actividad2_id)
        gastos_actividad3 = self.control_cuenta.listarGastos(self.actividad3_id)

        self.assertEqual(len(gastos_actividad1), 2)
        self.assertEqual(len(gastos_actividad2), 1)
        self.assertEqual(len(gastos_actividad3), 0)

    def test_crear_gasto_para_actividad(self):
        # Crear gasto con id de actividad nulo
        dia, mes, anho = self.parsear_fecha()
        crear_gasto_sin_actividad = self.control_cuenta.crearGastoParaActividad(
            None, self.viajero1_id, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, crear_gasto_sin_actividad[0])

        # Crear gasto con id de viajero nulo
        dia, mes, anho = self.parsear_fecha()
        crear_gasto_sin_viajero = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, 200, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, crear_gasto_sin_viajero[0])

        # Crear gasto con id de viajero fuera de actividad
        dia, mes, anho = self.parsear_fecha()
        crear_gasto_de_viajero_fuera_de_actividad = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero4_id, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, crear_gasto_de_viajero_fuera_de_actividad[0])

        # Crear gasto con datos de fecha errónea
        dia, mes, anho = self.parsear_fecha()
        crear_gasto_fecha_erronea = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero1_id, self.asignar_concepto(), -2020, 12, None, self.asignar_monto())
        self.assertEqual(False, crear_gasto_fecha_erronea[0])

        # Crear gasto con concepto nulo
        dia, mes, anho = self.parsear_fecha()
        crear_gasto_concepto_nulo = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero1_id, None, anho, mes, dia, 1234.43)
        self.assertEqual(False, crear_gasto_concepto_nulo[0])

        # Crear gasto con monto negativo
        dia, mes, anho = self.parsear_fecha()
        crear_gasto_monto_negativo = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero1_id, self.asignar_concepto(), anho, mes, dia, -1)
        self.assertEqual(False, crear_gasto_monto_negativo[0])

        # Crear gasto con concepto en blanco
        dia, mes, anho = self.parsear_fecha()
        crear_gasto_concepto_en_blanco = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero1_id, "", anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, crear_gasto_concepto_en_blanco[0])

        # Crear gasto con id de actividad nulo
        dia, mes, anho = self.parsear_fecha()
        self.control_cuenta.crearGastoParaActividad(self.actividad1_id, self.viajero1_id, self.gasto3_concepto, anho,
                                                    mes, dia, 5343.11)
        gasto_creado_con_exito = self.session.query(Gasto).filter(Gasto.actividad_id == self.actividad1_id,
                                                                  Gasto.concepto == self.gasto3_concepto).first()
        self.assertEqual([self.gasto3_concepto, "{:.2f}".format(5343.11)],
                         [gasto_creado_con_exito.concepto, "{:.2f}".format(gasto_creado_con_exito.monto)])

    def test_editar_gasto(self):
        # Editar gasto con id nulo
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_id_inexistente = self.control_cuenta.editarGasto(
            None, self.viajero1_id, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, editar_gasto_id_inexistente[0])

        # Editar gasto con id inexistente
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_id_nulo = self.control_cuenta.editarGasto(
            123, self.viajero1_id, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, editar_gasto_id_nulo[0])

        # Editar gasto con id de viajero nulo
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_sin_viajero = self.control_cuenta.editarGasto(
            self.gasto1_id, None, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, editar_gasto_sin_viajero[0])

        # Editar gasto con id de viajero inexistente
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_viajero_inexistente = self.control_cuenta.editarGasto(
            self.gasto3_id, 123, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, editar_gasto_viajero_inexistente[0])

        # Editar gasto con id de viajero que no pertenece a actividad
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_viajero_no_perteneciente_a_actividad = self.control_cuenta.editarGasto(
            self.gasto1_id, self.viajero4_id, self.asignar_concepto(), anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, editar_gasto_viajero_no_perteneciente_a_actividad[0])

        # Editar gasto con datos de fecha errónea
        editar_gasto_fecha_erronea = self.control_cuenta.editarGasto(
            self.gasto1_id, self.viajero1_id, self.asignar_concepto(), -2020, 12, None, self.asignar_monto())
        self.assertEqual(False, editar_gasto_fecha_erronea[0])

        # Editar gasto con concepto nulo
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_concepto_nulo = self.control_cuenta.editarGasto(
            self.gasto1_id, self.viajero1_id, None, anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, editar_gasto_concepto_nulo[0])

        # Editar gasto con concepto en blanco
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_concepto_blanco = self.control_cuenta.editarGasto(
            self.gasto1_id, self.viajero1_id, "", anho, mes, dia, self.asignar_monto())
        self.assertEqual(False, editar_gasto_concepto_blanco[0])

        # Editar gasto con monto negativo o distinto a número
        dia, mes, anho = self.parsear_fecha()
        editar_gasto_monto_negativo = self.control_cuenta.editarGasto(
            self.gasto3_id, self.viajero4_id, self.asignar_concepto(), anho, mes, dia, -1)
        self.assertEqual(False, editar_gasto_monto_negativo[0])

        # Editar gasto con éxito
        dia, mes, anho = self.parsear_fecha()
        self.control_cuenta.editarGasto(self.gasto3_id, self.viajero4_id, "Concepto específico", anho, mes, dia, 543.00)

        # Validación de actualización de datos de gasto
        gasto_editado_con_exito = self.session.query(Gasto).filter(Gasto.id == self.gasto3_id).first()
        self.assertEqual(["Concepto específico", "{:.2f}".format(543.00)],
                         [gasto_editado_con_exito.concepto, "{:.2f}".format(gasto_editado_con_exito.monto)])

    def test_eliminar_gasto(self):
        # Eliminar gasto con id nulo
        eliminar_sin_gasto_id = self.control_cuenta.eliminarGasto(None)
        self.assertEqual(False, eliminar_sin_gasto_id[0])

        # Eliminar gasto con id inexistente
        eliminar_gasto_inexistente = self.control_cuenta.eliminarGasto(300)
        self.assertEqual(False, eliminar_gasto_inexistente[0])

        # Eliminar gasto de actividad terminada
        eliminar_gasto_actividad_terminada = self.control_cuenta.eliminarGasto(self.gasto4_id)
        self.assertEqual(False, eliminar_gasto_actividad_terminada[0])

        # Eliminar gasto con actividad no terminada (éxito)
        cantidad_previa_eliminacion = self.session.query(Gasto).filter(Gasto.id == self.gasto1_id).count()
        self.control_cuenta.eliminarGasto(self.gasto1_id)
        cantidad_posterior_eliminacion = self.session.query(Gasto).filter(Gasto.id == self.gasto1_id).count()
        self.assertEqual(1, cantidad_previa_eliminacion)
        self.assertEqual(0, cantidad_posterior_eliminacion)

    def asignar_concepto(self):
        return self.data_factory.word()

    def asignar_monto(self):
        return round(random.uniform(1000, random.randint(1000, 15000)), 2)

    def asignar_fecha(self):
        return self.data_factory.date_between_dates(date_start=date(2019, 1, 1), date_end=date.today())

    def gasto_aleatorio(self, actividad_id, viajero_id):
        return Gasto(concepto=self.asignar_concepto(), monto=self.asignar_monto(), fecha=self.asignar_fecha(),
                     viajero_id=viajero_id, actividad_id=actividad_id)

    def parsear_fecha(self):
        dia, mes, anho = self.asignar_fecha().strftime("%d/%m/%Y").split("/")
        return int(dia), int(mes), int(anho)
