import unittest

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

        self.actividad1 = Actividad(nombre="Actividad de Ayrton", terminada=False)
        self.actividad2 = Actividad(nombre="Actividad de Pedro", terminada=False) 
        self.actividad3 = Actividad(nombre="Actividad de Raul", terminada=False)
        self.actividad4 = Actividad(nombre="Actividad de Dario", terminada=False)

        self.session.add_all([self.actividad1, self.actividad2, self.actividad3, self.actividad4])

        self.viajero1 = Viajero(nombre="Dario", apellido="Correal")
        self.viajero2 = Viajero(nombre="Ayrton", apellido="Pastor")
        self.viajero3 = Viajero(nombre="Pedro", apellido="Lizarazo")
        self.viajero4 = Viajero(nombre="Raul", apellido="Calero")

        self.session.add_all([self.viajero1, self.viajero2, self.viajero3, self.viajero4])
        self.session.flush()

        self.actividad_viajero1 = ActividadViajero(actividad_id=self.viajero1.id, viajero_id=self.actividad1.id)
        self.actividad_viajero2 = ActividadViajero(actividad_id=self.viajero2.id, viajero_id=self.actividad1.id)
        self.actividad_viajero3 = ActividadViajero(actividad_id=self.viajero3.id, viajero_id=self.actividad1.id)
        self.actividad_viajero4 = ActividadViajero(actividad_id=self.viajero4.id, viajero_id=self.actividad1.id)

        self.session.add_all([self.actividad_viajero1, self.actividad_viajero2, self.actividad_viajero3, self.actividad_viajero4])

        self.gasto1 = Gasto(concepto="paletas heladas", monto=1234, fecha=date(2021, 1, 1),
                            viajero_id=self.viajero1.id, actividad_id=self.actividad1.id)
        self.gasto2 = Gasto(concepto="alcohol", monto=4444, fecha=date(2021, 1, 4),
                            viajero_id=self.viajero3.id, actividad_id=self.actividad1.id)
        self.session.add_all([self.gasto1, self.gasto2])

        self.session.commit()
        self.actividad1_id = self.actividad1.id
        self.session.close()

    def tearDown(self):
        self.session = Session()

        actividad_viajeros = self.session.query(ActividadViajero).all()
        actividades = self.session.query(Actividad).all()
        viajeros = self.session.query(Viajero).all()

        for actividad_viajero in actividad_viajeros:
            self.session.delete(actividad_viajero)

        for actividad in actividades:
            self.session.delete(actividad)

        for viajero in viajeros:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()
    
    def test_listar_gastos(self):
        gastos = self.control_cuenta.listarGastos(self.actividad1_id)
        self.assertEqual(len(gastos), 2)


