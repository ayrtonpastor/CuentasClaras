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

        nombre_viajero1, apellido_viajero1 = self.asignar_nombre_y_apellido()
        nombre_viajero2, apellido_viajero2 = self.asignar_nombre_y_apellido()
        nombre_viajero3, apellido_viajero3 = self.asignar_nombre_y_apellido()

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
        # Listado de viajeros
        viajeros = self.control_cuenta.listarViajeros()
        self.assertEqual(len(viajeros), 3)

    def test_crear_viajero(self):
        # Crear viajero con nombre y apellidos vacíos o en blanco
        crear_viajero1 = self.control_cuenta.crearViajero(None, "")
        crear_viajero2 = self.control_cuenta.crearViajero("", None)
        self.assertEqual(False, crear_viajero1)
        self.assertEqual(False, crear_viajero2)

        # Crear viajero con nombre y apellido igual a otro viajero
        crear_viajero3 = self.control_cuenta.crearViajero(self.viajero3_nombre_original, self.viajero3_apellido_original)
        self.assertEqual(False, crear_viajero3)

        # Crear viajero sin errores
        nombre_viajero4, apellido_viajero4 = self.asignar_nombre_y_apellido()
        self.control_cuenta.crearViajero(nombre_viajero4, apellido_viajero4)
        viajero3 = self.session.query(Viajero).filter(Viajero.nombre == nombre_viajero4, Viajero.apellido == apellido_viajero4).first()
        self.assertTrue(nombre_viajero4, viajero3.nombre)

    def test_editar_viajero(self):
        # Editar viajero con nombre en blanco o apellido nulo
        self.control_cuenta.editarViajero(self.viajero1_id, "", None)
        viajero1 = self.session.query(Viajero).filter(Viajero.id == self.viajero1_id).first()
        self.assertEqual(self.viajero1_nombre_original, viajero1.nombre)

        # Editar viajero con id inexistente
        nuevo_nombre1, nuevo_apellido1 = self.asignar_nombre_y_apellido()
        editar_viajero_inexistente = self.control_cuenta.editarViajero(200, nuevo_nombre1, nuevo_apellido1)
        self.assertEqual(False, editar_viajero_inexistente)

        # Editar viajero con nombre y apellido igual a otro viajero
        self.control_cuenta.editarViajero(self.viajero2_id, self.viajero3_nombre_original, self.viajero3_apellido_original)
        viajero2 = self.session.query(Viajero).filter(Viajero.id == self.viajero2_id).first()
        self.assertEqual(self.viajero2_nombre_original, viajero2.nombre)

        # Editar viajero con éxito
        nuevo_nombre3, nuevo_apellido3 = self.asignar_nombre_y_apellido()
        self.control_cuenta.editarViajero(self.viajero3_id, nuevo_nombre3, nuevo_apellido3)
        viajero3 = self.session.query(Viajero).filter(Viajero.id == self.viajero3_id).first()
        self.assertEqual([nuevo_nombre3, nuevo_apellido3], [viajero3.nombre, viajero3.apellido])

    def test_eliminar_viajero(self):
        # Eliminar viajero con id nulo
        eliminar_viajero_con_id_nulo = self.control_cuenta.eliminarViajero(None)
        self.assertEqual(False, eliminar_viajero_con_id_nulo[0])

        # Eliminar viajero con id inexistente
        eliminar_viajero_inexistente = self.control_cuenta.eliminarViajero(231)
        self.assertEqual(False, eliminar_viajero_inexistente[0])

        # Eliminar viajero con gastos
        eliminar_viajero_en_actividad_con_gastos = self.control_cuenta.eliminarViajero(self.viajero2_id)
        self.assertEqual(False, eliminar_viajero_en_actividad_con_gastos[0])

        # Eliminar viajero sin gastos pero perteneciente a actividades
        eliminar_viajero_en_actividad_sin_gastos = self.control_cuenta.eliminarViajero(self.viajero1_id)
        self.assertEqual(False, eliminar_viajero_en_actividad_sin_gastos[0])

        # Eliminar viajero sin gastos y sin pertenecer a ninguna actividad (con éxito)
        # validación de existencia de viajero previa eliminación
        viajero_previa_eliminacion = self.session.query(Viajero).filter(Viajero.id == self.viajero3_id).count()
        self.assertEqual(1, viajero_previa_eliminacion)

        self.control_cuenta.eliminarViajero(self.viajero3_id)

        # validación existencia de viajero después de eliminar
        viajero_posterior_eliminacion = self.session.query(Viajero).filter(Viajero.id == self.viajero3_id).count()
        self.assertEqual(0, viajero_posterior_eliminacion)

    def asignar_nombre_y_apellido(self):
        # método que retorna un nombre y apellido aleatorio para el viajero
        return [self.data_factory.name(), self.data_factory.name()]
