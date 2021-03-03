import unittest

from src.logica.control_cuenta import ControlCuenta
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session


class ViajeroTestCase(unittest.TestCase):
    def setUp(self):
        """ Crear Control cuenta"""
        self.control_cuenta = ControlCuenta()
        self.session = Session()

    def tearDown(self):
        self.session = Session()

        viajeros = self.session.query(Viajero).all()

        for viajero in viajeros:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()

    def test_crear_viajero(self):
        nombre_viajero1 = None
        apellido_viajero1 = None
        nombre_viajero2 = ""
        apellido_viajero2 = ""
        nombre_viajero3 = "Jhon"
        apellido_viajero3 = "Arismendiz"

        result1 = self.control_cuenta.crearViajero(nombre_viajero1, apellido_viajero1)
        result2 = self.control_cuenta.crearViajero(nombre_viajero2, apellido_viajero2)
        result3 = self.control_cuenta.crearViajero(nombre_viajero3, apellido_viajero3)

        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertTrue(result3)
