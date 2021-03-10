import unittest

from faker import Faker
from src.logica.control_cuenta import ControlCuenta
from src.modelo.declarative_base import Session
from src.modelo.viajero import Viajero


class ViajeroTestCase(unittest.TestCase):
    def setUp(self):
        """ Crear Control cuenta"""
        self.control_cuenta = ControlCuenta()
        self.session = Session()
        """ Generación de datos aleatorios """
        self.data_factory = Faker()
        
        self.viajero1 = Viajero(nombre="Dario", apellido="Correal")
        self.viajero2 = Viajero(nombre="Ayrton", apellido="Pastor")
        self.viajero3 = Viajero(nombre="Pedro", apellido="Lizarazo")

        self.session.add_all([self.viajero1, self.viajero2, self.viajero3])
        self.session.flush()

        self.session.commit()

        self.viajero1_id = self.viajero1.id
        self.viajero2_id = self.viajero2.id
        self.viajero3_id = self.viajero3.id

        self.session.close()

    def tearDown(self):
        self.session = Session()

        viajeros = self.session.query(Viajero).all()

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
        nuevo_nombre2 = "Pedro"
        nuevo_apellido2 = "Lizarazo"
        nuevo_nombre3 = "Juan"
        nuevo_apellido3 = "Flores"

        self.control_cuenta.editarViajero(self.viajero1_id, nuevo_nombre1, nuevo_apellido1)
        self.control_cuenta.editarViajero(self.viajero2_id, nuevo_nombre2, nuevo_apellido2)
        self.control_cuenta.editarViajero(self.viajero3_id, nuevo_nombre3, nuevo_apellido3)
        editar_viajero_inexistente = self.control_cuenta.editarViajero(200, nuevo_nombre2, nuevo_apellido2)

        viajero1 = self.session.query(Viajero).filter(Viajero.id == self.viajero1_id).first()
        viajero2 = self.session.query(Viajero).filter(Viajero.id == self.viajero2_id).first()
        viajero3 = self.session.query(Viajero).filter(Viajero.id == self.viajero3_id).first()

        self.assertEqual("Dario", viajero1.nombre)
        self.assertEqual("Ayrton", viajero2.nombre)
        self.assertEqual("Juan", viajero3.nombre)
        self.assertEqual(False, editar_viajero_inexistente)
