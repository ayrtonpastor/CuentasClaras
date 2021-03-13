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

        nombre_actividad1 = self.data_factory.name()
        nombre_actividad2 = self.data_factory.name()
        nombre_actividad3 = self.data_factory.name()

        self.actividad1 = Actividad(nombre=nombre_actividad1, terminada=False)
        self.actividad2 = Actividad(nombre=nombre_actividad2, terminada=False)
        self.actividad3 = Actividad(nombre=nombre_actividad3, terminada=False)

        self.session.add_all([self.actividad1, self.actividad2, self.actividad3])

        nombre_viajero1 = self.data_factory.name()
        nombre_viajero2 = self.data_factory.name()
        nombre_viajero3 = self.data_factory.name()
        nombre_viajero4 = self.data_factory.name()

        apellido_viajero1 = self.data_factory.name()
        apellido_viajero2 = self.data_factory.name()
        apellido_viajero3 = self.data_factory.name()
        apellido_viajero4 = self.data_factory.name()

        self.viajero1 = Viajero(nombre=nombre_viajero1, apellido=apellido_viajero1)
        self.viajero2 = Viajero(nombre=nombre_viajero2, apellido=apellido_viajero2)
        self.viajero3 = Viajero(nombre=nombre_viajero3, apellido=apellido_viajero3)
        self.viajero4 = Viajero(nombre=nombre_viajero4, apellido=apellido_viajero4)

        self.session.add_all([self.viajero1, self.viajero2, self.viajero3, self.viajero4])
        self.session.flush()

        # Viajeros asociados a actividad 1
        self.actividad_viajero1 = ActividadViajero(
            actividad_id=self.actividad1.id, viajero_id=self.viajero1.id)
        self.actividad_viajero2 = ActividadViajero(
            actividad_id=self.actividad1.id, viajero_id=self.viajero2.id)

        # Viajeros asociados a actividad 2
        self.actividad_viajero3 = ActividadViajero(
            actividad_id=self.actividad2.id, viajero_id=self.viajero3.id)
        self.actividad_viajero4 = ActividadViajero(
            actividad_id=self.actividad2.id, viajero_id=self.viajero4.id)

        self.session.add_all([self.actividad_viajero1, self.actividad_viajero2, self.actividad_viajero3,
                              self.actividad_viajero4])

        concepto_gasto1 = self.data_factory.name()
        concepto_gasto2 = self.data_factory.name()
        concepto_gasto3 = self.data_factory.name()

        monto_gasto1 = round(random.uniform(1000, 10000), 2)
        monto_gasto2 = round(random.uniform(1234, 15928), 2)
        monto_gasto3 = round(random.uniform(9923, 14765), 2)

        fecha_gasto1 = self.data_factory.date_between_dates(date_start=date(2019, 1, 1), date_end=date.today())
        fecha_gasto2 = self.data_factory.date_between_dates(date_start=date(2019, 1, 1), date_end=date.today())
        fecha_gasto3 = self.data_factory.date_between_dates(date_start=date(2019, 1, 1), date_end=date.today())

        # Gastos asociados a la actividad 1
        self.gasto1 = Gasto(concepto=concepto_gasto1, monto=monto_gasto1, fecha=fecha_gasto1,
                            viajero_id=self.viajero1.id, actividad_id=self.actividad1.id)
        self.gasto2 = Gasto(concepto=concepto_gasto2, monto=monto_gasto2, fecha=fecha_gasto2,
                            viajero_id=self.viajero2.id, actividad_id=self.actividad1.id)

        # Gastos asociados a la actividad 2
        self.gasto3 = Gasto(concepto=concepto_gasto3, monto=monto_gasto3, fecha=fecha_gasto3,
                            viajero_id=self.viajero3.id, actividad_id=self.actividad2.id)
        self.session.add_all([self.gasto1, self.gasto2, self.gasto3])

        self.session.commit()

        self.gasto1_concepto = self.gasto1.concepto
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
        gastos_actividad1 = self.control_cuenta.listarGastos(self.actividad1_id)
        gastos_actividad2 = self.control_cuenta.listarGastos(self.actividad2_id)
        gastos_actividad3 = self.control_cuenta.listarGastos(self.actividad3_id)

        self.assertEqual(len(gastos_actividad1), 2)
        self.assertEqual(len(gastos_actividad2), 1)
        self.assertEqual(len(gastos_actividad3), 0)

    def test_crear_gasto_para_actividad(self):
        crear_gasto_sin_actividad = self.control_cuenta.crearGastoParaActividad(
            None, self.viajero1_id, "Concepto gasto 1", 2020, 12, 4, 1234.43)
        crear_gasto_sin_viajero = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, 200, "Concepto gasto 2", 2020, 12, 4, 1234.43)
        crear_gasto_de_viajero_fuera_de_actividad = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero4_id, "Concepto gasto 3", 2020, 12, 4, 1234.43)
        crear_gasto_fecha_erronea = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero1_id, "Concepto gasto 4", -2020, 12, None, 1234.43)
        crear_gasto_concepto_nulo = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero1_id, None, 2020, 12, 12, 1234.43)
        crear_gasto_monto_negativo = self.control_cuenta.crearGastoParaActividad(
            self.actividad1_id, self.viajero1_id, "Concepto gasto 6", 2020, 12, 12, -4444.43)

        self.assertEqual(False, crear_gasto_sin_actividad)
        self.assertEqual(False, crear_gasto_sin_viajero)
        self.assertEqual(False, crear_gasto_de_viajero_fuera_de_actividad)
        self.assertEqual(False, crear_gasto_fecha_erronea)
        self.assertEqual(False, crear_gasto_concepto_nulo)
        self.assertEqual(False, crear_gasto_monto_negativo)
