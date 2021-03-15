import unittest

from datetime import date
from faker import Faker
from src.logica.control_cuenta import ControlCuenta
from src.modelo.actividad import Actividad, ActividadViajero
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Session
from sqlalchemy.exc import IntegrityError


class ActividadTestCase(unittest.TestCase):
    def setUp(self):
        """ Crear Control cuenta"""
        self.control_cuenta = ControlCuenta()
        self.session = Session()
        """ Generación de datos aleatorios """
        self.data_factory = Faker()

        self.actividad1 = Actividad(nombre=self.data_factory.word(), terminada=False)
        self.actividad2 = Actividad(nombre=self.data_factory.word(), terminada=False)
        self.actividad3 = Actividad(nombre=self.data_factory.word(), terminada=False)
        self.actividad4 = Actividad(nombre=self.data_factory.word(), terminada=False)

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

        # Viajero asociado a actividad 3
        self.actividad_viajero5 = ActividadViajero(actividad_id=self.actividad3.id, viajero_id=self.viajero4.id)
        self.actividad_viajero6 = ActividadViajero(actividad_id=self.actividad3.id, viajero_id=self.viajero1.id)

        self.session.add_all([self.actividad_viajero1, self.actividad_viajero2, self.actividad_viajero3,
                              self.actividad_viajero4, self.actividad_viajero5, self.actividad_viajero6])

        # Gastos asociados a la actividad 1
        self.gasto1 = Gasto(concepto=self.data_factory.word(), monto=1234, fecha=self.asignar_fecha(),
                            viajero_id=self.viajero1.id, actividad_id=self.actividad1.id)
        self.gasto2 = Gasto(concepto=self.data_factory.word(), monto=4444, fecha=self.asignar_fecha(),
                            viajero_id=self.viajero2.id, actividad_id=self.actividad1.id)

        # Gastos asociados a la actividad 2
        self.gasto3 = Gasto(concepto=self.data_factory.word(), monto=999.24, fecha=self.asignar_fecha(),
                            viajero_id=self.viajero3.id, actividad_id=self.actividad2.id)

        self.session.add_all([self.gasto1, self.gasto2, self.gasto3])

        self.session.commit()

        self.actividad1_id = self.actividad1.id
        self.actividad2_id = self.actividad2.id
        self.actividad3_id = self.actividad3.id
        self.actividad4_id = self.actividad4.id

        self.viajero1_id = self.viajero1.id
        self.viajero2_id = self.viajero2.id
        self.viajero3_id = self.viajero3.id
        self.viajero4_id = self.viajero4.id

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

    def test_listar_actividades(self):
        actividades = self.control_cuenta.listarActividades()
        self.assertEqual(len(actividades), 4)

    def test_reporte_compensacion_sin_viajeros(self):
        """ Solo aparecerá la primera celda de la tabla """
        reporte_compensacion = self.control_cuenta.crearReporteCompensacion(
            self.actividad4_id)
        self.assertListEqual([[" "]], reporte_compensacion)

    def test_reporte_compensacion_sin_gastos(self):
        """ Solo aparecerá la cabecera de la tabla """
        reporte_compensacion = self.control_cuenta.crearReporteCompensacion(
            self.actividad3_id)

        viajero1 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero1_id).first()
        viajero4 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero4_id).first()

        self.assertEqual([
            [" ", viajero1.nombre_completo(), viajero4.nombre_completo()]
        ], reporte_compensacion)

    def test_reporte_compensacion_actividad(self):
        reporte_compensacion_actividad_1 = self.control_cuenta.crearReporteCompensacion(
            self.actividad1_id)

        viajero1 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero1_id).first()
        viajero2 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero2_id).first()
        viajero3 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero3_id).first()
        viajero4 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero4_id).first()

        self.assertEqual([
            [" ", viajero1.nombre_completo(), viajero2.nombre_completo()],
            [viajero1.nombre_completo(), -1, "1605.00"],
            [viajero2.nombre_completo(), "0.00", -1]
        ], reporte_compensacion_actividad_1)

        reporte_compensacion_actividad_2 = self.control_cuenta.crearReporteCompensacion(
            self.actividad2_id)
        self.assertEqual([
            [" ", viajero3.nombre_completo(), viajero4.nombre_completo()],
            [viajero3.nombre_completo(), -1, "0.00"],
            [viajero4.nombre_completo(), "499.62", -1]
        ], reporte_compensacion_actividad_2)

    def test_reporte_gastos_por_viajero_en_actividad(self):
        reporte_gastos_por_viajero_actividad4 = self.control_cuenta.crearReporteGastosPorViajero(
            self.actividad4_id)
        reporte_gastos_por_viajero_actividad3 = self.control_cuenta.crearReporteGastosPorViajero(
            self.actividad3_id)
        reporte_gastos_por_viajero_actividad2 = self.control_cuenta.crearReporteGastosPorViajero(
            self.actividad2_id)
        reporte_gastos_por_viajero_actividad1 = self.control_cuenta.crearReporteGastosPorViajero(
            self.actividad1_id)

        viajero1 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero1_id).first()
        viajero2 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero2_id).first()
        viajero3 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero3_id).first()
        viajero4 = self.session.query(Viajero).filter(
            Viajero.id == self.viajero4_id).first()

        self.assertEqual([], reporte_gastos_por_viajero_actividad4)
        self.assertEqual([
            {"Nombre": viajero1.nombre, "Apellido": viajero1.apellido, "Valor": "0.00"},
            {"Nombre": viajero4.nombre, "Apellido": viajero4.apellido, "Valor": "0.00"}
        ], reporte_gastos_por_viajero_actividad3)
        self.assertEqual([
            {"Nombre": viajero3.nombre,
                "Apellido": viajero3.apellido, "Valor": "999.24"},
            {"Nombre": viajero4.nombre, "Apellido": viajero4.apellido, "Valor": "0.00"}
        ], reporte_gastos_por_viajero_actividad2)
        self.assertEqual([
            {"Nombre": viajero1.nombre,
                "Apellido": viajero1.apellido, "Valor": "1234.00"},
            {"Nombre": viajero2.nombre,
                "Apellido": viajero2.apellido, "Valor": "4444.00"}
        ], reporte_gastos_por_viajero_actividad1)

    def test_crear_actividad(self):
        self.assertEqual(None, self.control_cuenta.crearActividad(None))

        self.control_cuenta.crearActividad("")
        actividad_vacia = self.session.query(
            Actividad).filter(Actividad.nombre == "").first()
        # No pueden existir actividades vacias
        self.assertEqual(actividad_vacia, None)

        self.control_cuenta.crearActividad("integracion")
        actividad_con_nombre = self.session.query(Actividad).filter(
            Actividad.nombre == "integracion").first()
        self.assertNotEqual(actividad_con_nombre, None)
        nombre_actividad = actividad_con_nombre.nombre
        self.assertEqual(nombre_actividad, "integracion")

        with self.assertRaises(IntegrityError):
            self.control_cuenta.crearActividad("integracion")

    def test_asociar_viajero_a_actividad(self):
        self.assertEqual(
            None, self.control_cuenta.asociarViajeroAActividad(None, None))

        self.control_cuenta.asociarViajeroAActividad(
            actividad_id=self.actividad4_id, viajero_id=self.viajero4_id)
        actividad_viajero = self.session.query(ActividadViajero).filter(ActividadViajero.actividad_id ==
                                                                        self.actividad4_id, ActividadViajero.viajero_id == self.viajero4_id).first()
        self.assertEqual(actividad_viajero.actividad_id, self.actividad4_id)
        self.assertEqual(actividad_viajero.viajero_id, self.viajero4_id)

        # El viajero no existe
        self.session = Session()
        self.session.delete(self.viajero4)
        self.session.commit()
        self.session.close()
        with self.assertRaises(Exception):
            self.control_cuenta.asociarViajeroAActividad(
                actividad_id=self.actividad4_id, viajero_id=self.viajero4_id)

    def test_retirar_viajero_actividad(self):
        self.assertEqual(
            None, self.control_cuenta.eliminarActividadViajero(None, None))

        # Viajero con gastos
        with self.assertRaises(Exception):
            self.control_cuenta.eliminarActividadViajero(
                self.actividad1_id, self.viajero1_id)

        # Actividad terminada
        self.session = Session()
        self.actividad1.terminada = True
        self.session.add(self.actividad1)
        self.session.commit()

        with self.assertRaises(Exception):
            self.control_cuenta.eliminarActividadViajero(
                self.actividad1_id, self.viajero1_id)

        # Eliminacion efectiva
        self.control_cuenta.eliminarActividadViajero(
            self.actividad3_id, self.viajero1_id)
        count = self.session.query(ActividadViajero).filter(ActividadViajero.actividad_id ==
                                                            self.actividad3_id, ActividadViajero.viajero_id == self.viajero1_id).count()
        self.assertEqual(0, count)

        self.session.close()

    def test_eliminar_actividad(self):
        self.assertEqual(
            None, self.control_cuenta.eliminarActividad(None))

        # Actividad con gastos
        with self.assertRaises(Exception):
            self.control_cuenta.eliminarActividad(
                self.actividad1_id)

        # Actividad terminada (actividad2)
        self.session = Session()
        self.actividad4.terminada = True
        self.session.add(self.actividad4)
        self.session.commit()
        with self.assertRaises(Exception):
            self.control_cuenta.eliminarActividad(
                self.actividad4_id)

        self.actividad4.terminada = False
        self.session.add(self.actividad4)
        self.session.commit()

        self.session.close()

        # Actividad sin gastos ni terminada
        self.control_cuenta.eliminarActividad(
            self.actividad4_id)
        count = self.session.query(Actividad).filter(Actividad.id ==
                                                     self.actividad4_id).count()
        self.assertEqual(0, count)
    
    def test_editar_actividad(self):
        self.assertEqual(
            None, self.control_cuenta.editarActividad(None,None))
        
        #Nombre vacio
        with self.assertRaises(Exception):
            self.control_cuenta.editarActividad(
                self.actividad1_id, "")
        
        #Cambio cuando actividad está terminada
        nombre_valido = "Valid name not created before"
        count = self.session.query(Actividad).filter(
            Actividad.nombre == nombre_valido).count()
        self.assertEqual(0, count)

        self.session = Session()
        self.actividad4.terminada = True
        self.session.add(self.actividad4)
        self.session.commit()

        with self.assertRaises(Exception):
            self.control_cuenta.editarActividad(
                self.actividad4_id, nombre_valido)

        _actividad = self.session.query(Actividad).filter(
            Actividad.id == self.actividad4_id).first()
        self.assertNotEqual(nombre_valido, _actividad.nombre)

        self.actividad4.terminada = False
        self.session.add(self.actividad4)
        self.session.commit()
        
        self.session.close()
        
        #Cambio nombre actividad 4 a un nombre repetido de actividad 1
        nombre_repetido = self.actividad1.nombre
        with self.assertRaises(Exception):
            self.control_cuenta.editarActividad(
                self.actividad4_id, nombre_repetido)
        
        #Cambio nombre a uno valido
        nombre_valido = "Valid name not created before"
        count = self.session.query(Actividad).filter(
            Actividad.nombre == nombre_valido).count()
        self.assertEqual(0, count)
        self.control_cuenta.editarActividad(self.actividad4_id, nombre_valido)
        count = self.session.query(Actividad).filter(
            Actividad.nombre == nombre_valido).count()
        self.assertEqual(1, count)

    def test_terminar_actividad(self):
        terminar_actividad_con_id_nulo = self.control_cuenta.terminarActividad(None)
        terminar_actividad_con_id_inexistente = self.control_cuenta.terminarActividad(123)

        self.assertEqual(False, terminar_actividad_con_id_nulo[0])
        self.assertEqual(False, terminar_actividad_con_id_inexistente[0])

        self.control_cuenta.terminarActividad(self.actividad1_id)
        actividad = self.session.query(Actividad).filter(Actividad.id == self.actividad1_id).first()
        self.assertEqual(True, actividad.terminada)

    def asignar_fecha(self):
        return self.data_factory.date_between_dates(date_start=date(2019, 1, 1), date_end=date.today())
