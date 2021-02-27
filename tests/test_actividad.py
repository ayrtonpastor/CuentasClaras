import unittest

from src.logica.control_cuenta import ControlCuenta
from src.modelo.actividad import Actividad
from src.modelo.declarative_base import Session

class ActividadTestCase(unittest.TestCase):
    def setUp(self):
        ''' Crear Control cuenta'''
        self.control_cuenta = ControlCuenta()
        self.session = Session()

        self.actividad1 = Actividad(nombre="Actividad de Ayrton", terminada=False)
        self.actividad2 = Actividad(nombre="Actividad de Pedro", terminada=False) 
        self.actividad3 = Actividad(nombre="Actividad de Raul", terminada=False)
        self.actividad4 = Actividad(nombre="Actividad de Dario", terminada=False)

        self.session.add(self.actividad1)
        self.session.add(self.actividad2)
        self.session.add(self.actividad3)
        self.session.add(self.actividad4)
        
        self.session.commit()
        self.session.close()

    def tearDown(self):
        '''Abre la sesion'''
        self.session = Session()

        '''Consulta todas las actividades'''
        busqueda = self.session.query(Actividad).all()

        '''Borra todas las actividades'''
        for actividad in busqueda:
            self.session.delete(actividad)

        self.session.commit()
        self.session.close()
    
    def test_listar_actividades(self):
        actividades = self.control_cuenta.listarActividades()
        self.assertEqual(len(actividades), 4)


