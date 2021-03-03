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
        result = self.control_cuenta.crearViajero(nombre_viajero1, apellido_viajero1)
        self.assertFalse(result)
