import unittest

from src.logica.control_cuenta import ControlCuenta
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session


class ViajeroTestCase(unittest.TestCase):
    def setUp(self):
        """ Crear Control cuenta"""
        self.control_cuenta = ControlCuenta()
        self.session = Session()
        
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
        apellido_viajero1 = None
        nombre_viajero2 = ""
        apellido_viajero2 = ""
        nombre_viajero3 = "Jhon"
        apellido_viajero3 = "Arismendiz"
        nombre_viajero4 = "Jhon"
        apellido_viajero4 = "Arismendiz"

        result1 = self.control_cuenta.crearViajero(nombre_viajero1, apellido_viajero1)
        result2 = self.control_cuenta.crearViajero(nombre_viajero2, apellido_viajero2)
        result3 = self.control_cuenta.crearViajero(nombre_viajero3, apellido_viajero3)
        result4 = self.control_cuenta.crearViajero(nombre_viajero4, apellido_viajero4)

        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertTrue(result3)
        self.assertFalse(result4)

    def test_editar_viajero(self):
        nuevo_nombre1 = ""
        nuevo_apellido1 = None
        nuevo_nombre2 = "Pedro"
        nuevo_apellido2 = "Lizarazo"

        self.control_cuenta.editarViajero(self.viajero1_id, nuevo_nombre1, nuevo_apellido1)
        self.control_cuenta.editarViajero(self.viajero2_id, nuevo_nombre2, nuevo_apellido2)
        editar_viajero_inexistente = self.control_cuenta.editarViajero(200, nuevo_nombre2, nuevo_apellido2)

        viajero1 = self.session.query(Viajero).filter(Viajero.id == self.viajero1_id).first()
        viajero2 = self.session.query(Viajero).filter(Viajero.id == self.viajero2_id).first()

        self.assertEqual("Dario", viajero1.nombre)
        self.assertEqual("Pedro", viajero2.nombre)
        self.assertEqual(False, editar_viajero_inexistente)
