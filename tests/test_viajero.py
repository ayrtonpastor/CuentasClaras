import random
import unittest

from datetime import date
from faker import Faker
from src.logica.control_cuenta import ControlCuenta
from src.modelo.actividad import Actividad, ActividadViajero
from src.modelo.declarative_base import Session
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero


class ViajeroTestCase(unittest.TestCase):
    def setUp(self):
        """ Crear Control cuenta"""
        self.control_cuenta = ControlCuenta()
        self.session = Session()
        """ Generación de datos aleatorios """
        self.data_factory = Faker()

        nombre_actividad1 = self.data_factory.word()
        self.actividad1 = Actividad(nombre=nombre_actividad1, terminada=False)

        self.session.add_all([self.actividad1])

        nombre_viajero1 = self.data_factory.name()
        nombre_viajero2 = self.data_factory.name()
        nombre_viajero3 = self.data_factory.name()

        apellido_viajero1 = self.data_factory.name()
        apellido_viajero2 = self.data_factory.name()
        apellido_viajero3 = self.data_factory.name()

        self.viajero1 = Viajero(nombre=nombre_viajero1, apellido=apellido_viajero1)
        self.viajero2 = Viajero(nombre=nombre_viajero2, apellido=apellido_viajero2)
        self.viajero3 = Viajero(nombre=nombre_viajero3, apellido=apellido_viajero3)

        self.session.add_all([self.viajero1, self.viajero2, self.viajero3])
        self.session.flush()

        # Viajeros asociados a actividad 1
        self.actividad_viajero1 = ActividadViajero(actividad_id=self.actividad1.id, viajero_id=self.viajero1.id)
        self.actividad_viajero2 = ActividadViajero(actividad_id=self.actividad1.id, viajero_id=self.viajero2.id)

        self.session.add_all([self.actividad_viajero1, self.actividad_viajero2])

        # Gasto de viajero 2
        concepto_gasto1 = self.data_factory.word()
        monto_gasto1 = round(random.uniform(1000, random.randint(1000, 15000)), 2)
        fecha_gasto1 = self.data_factory.date_between_dates(date_start=date(2019, 1, 1), date_end=date.today())

        self.gasto1 = Gasto(concepto=concepto_gasto1, monto=monto_gasto1, fecha=fecha_gasto1,
                            viajero_id=self.viajero2.id, actividad_id=self.actividad1.id)
        self.session.add_all([self.gasto1])

        self.session.commit()

        self.viajero1_id = self.viajero1.id
        self.viajero2_id = self.viajero2.id
        self.viajero3_id = self.viajero3.id

        self.viajero1_nombre_original = self.viajero1.nombre
        self.viajero2_nombre_original = self.viajero2.nombre
        self.viajero3_nombre_original = self.viajero3.nombre
        self.viajero3_apellido_original = self.viajero3.apellido

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

    def test_listar_viajeros(self):
        viajeros = self.control_cuenta.listarViajeros()
        self.assertEqual(len(viajeros), 3)

    def test_crear_viajero(self):
        nombre_viajero1 = None
        apellido_viajero1 = ""
        nombre_viajero2 = ""
        apellido_viajero2 = None
        nombre_viajero3 = self.data_factory.name()
        apellido_viajero3 = self.data_factory.name()
        nombre_viajero4 = nombre_viajero3
        apellido_viajero4 = apellido_viajero3

        crear_viajero1 = self.control_cuenta.crearViajero(nombre_viajero1, apellido_viajero1)
        crear_viajero2 = self.control_cuenta.crearViajero(nombre_viajero2, apellido_viajero2)
        self.control_cuenta.crearViajero(nombre_viajero3, apellido_viajero3)
        crear_viajero4 = self.control_cuenta.crearViajero(nombre_viajero4, apellido_viajero4)

        viajero3 = self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero3, Viajero.apellido == apellido_viajero3).first()

        self.assertEqual(False, crear_viajero1)
        self.assertEqual(False, crear_viajero2)
        self.assertTrue(nombre_viajero3, viajero3.nombre)
        self.assertEqual(False, crear_viajero4)

    def test_editar_viajero(self):
        nuevo_nombre1 = ""
        nuevo_apellido1 = None
        nuevo_nombre2 = self.viajero3_nombre_original
        nuevo_apellido2 = self.viajero3_apellido_original
        nuevo_nombre3 = self.data_factory.name()
        nuevo_apellido3 = self.data_factory.name()

        self.control_cuenta.editarViajero(self.viajero1_id, nuevo_nombre1, nuevo_apellido1)
        self.control_cuenta.editarViajero(self.viajero2_id, nuevo_nombre2, nuevo_apellido2)
        self.control_cuenta.editarViajero(self.viajero3_id, nuevo_nombre3, nuevo_apellido3)
        editar_viajero_inexistente = self.control_cuenta.editarViajero(200, nuevo_nombre2, nuevo_apellido2)

        viajero1 = self.session.query(Viajero).filter(Viajero.id == self.viajero1_id).first()
        viajero2 = self.session.query(Viajero).filter(Viajero.id == self.viajero2_id).first()
        viajero3 = self.session.query(Viajero).filter(Viajero.id == self.viajero3_id).first()

        self.assertEqual(self.viajero1_nombre_original, viajero1.nombre)
        self.assertEqual(self.viajero2_nombre_original, viajero2.nombre)
        self.assertEqual([nuevo_nombre3, nuevo_apellido3], [viajero3.nombre, viajero3.apellido])
        self.assertEqual(False, editar_viajero_inexistente)

    def test_eliminar_viajero(self):
        eliminar_viajero_con_id_nulo = self.control_cuenta.eliminarViajero(None)
        eliminar_viajero_inexistente = self.control_cuenta.eliminarViajero(231)
        eliminar_viajero_en_actividad_sin_gastos = self.control_cuenta.eliminarViajero(self.viajero1_id)
        eliminar_viajero_en_actividad_con_gastos = self.control_cuenta.eliminarViajero(self.viajero2_id)

        self.assertEqual(False, eliminar_viajero_con_id_nulo[0])
        self.assertEqual(False, eliminar_viajero_inexistente[0])
        self.assertEqual(False, eliminar_viajero_en_actividad_sin_gastos[0])
        self.assertEqual(False, eliminar_viajero_en_actividad_con_gastos[0])

        viajero_previa_eliminacion = self.session.query(Viajero).filter(Viajero.id == self.viajero3_id).count()
        self.control_cuenta.eliminarViajero(self.viajero3_id)
        viajero_posterior_eliminacion = self.session.query(Viajero).filter(Viajero.id == self.viajero3_id).count()

        self.assertEqual(1, viajero_previa_eliminacion)
        self.assertEqual(0, viajero_posterior_eliminacion)
