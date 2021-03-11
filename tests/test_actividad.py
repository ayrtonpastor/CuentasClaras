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

        nombre_actividad1 = self.data_factory.name()
        nombre_actividad2 = self.data_factory.name()
        nombre_actividad3 = self.data_factory.name()
        nombre_actividad4 = self.data_factory.name()

        self.actividad1 = Actividad(nombre=nombre_actividad1, terminada=False)
        self.actividad2 = Actividad(nombre=nombre_actividad2, terminada=False)
        self.actividad3 = Actividad(nombre=nombre_actividad3, terminada=False)
        self.actividad4 = Actividad(nombre=nombre_actividad4, terminada=False)

        self.session.add_all(
            [self.actividad1, self.actividad2, self.actividad3, self.actividad4])

        nombre_viajero1 = self.data_factory.name()
        nombre_viajero2 = self.data_factory.name()
        nombre_viajero3 = self.data_factory.name()
        nombre_viajero4 = self.data_factory.name()

        apellido_viajero1 = self.data_factory.name()
        apellido_viajero2 = self.data_factory.name()
        apellido_viajero3 = self.data_factory.name()
        apellido_viajero4 = self.data_factory.name()

        self.viajero1 = Viajero(nombre=nombre_viajero1,
                                apellido=apellido_viajero1)
        self.viajero2 = Viajero(nombre=nombre_viajero2,
                                apellido=apellido_viajero2)
        self.viajero3 = Viajero(nombre=nombre_viajero3,
                                apellido=apellido_viajero3)
        self.viajero4 = Viajero(nombre=nombre_viajero4,
                                apellido=apellido_viajero4)

        self.session.add_all(
            [self.viajero1, self.viajero2, self.viajero3, self.viajero4])
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

        # Viajero asociado a actividad 3
        self.actividad_viajero5 = ActividadViajero(
            actividad_id=self.actividad3.id, viajero_id=self.viajero4.id)
        self.actividad_viajero6 = ActividadViajero(
            actividad_id=self.actividad3.id, viajero_id=self.viajero1.id)

        self.session.add_all([self.actividad_viajero1, self.actividad_viajero2, self.actividad_viajero3,
                              self.actividad_viajero4, self.actividad_viajero5, self.actividad_viajero6])

        # Gastos asociados a la actividad 1
        concepto_gasto1 = self.data_factory.name()
        concepto_gasto2 = self.data_factory.name()
        concepto_gasto3 = self.data_factory.name()

        self.gasto1 = Gasto(concepto=concepto_gasto1, monto=1234, fecha=date(2021, 1, 1),
                            viajero_id=self.viajero1.id, actividad_id=self.actividad1.id)
        self.gasto2 = Gasto(concepto=concepto_gasto2, monto=4444, fecha=date(2021, 1, 4),
                            viajero_id=self.viajero2.id, actividad_id=self.actividad1.id)

        # Gastos asociados a la actividad 2
        self.gasto3 = Gasto(concepto=concepto_gasto3, monto=999.24, fecha=date(
            2020, 1, 1), viajero_id=self.viajero3.id, actividad_id=self.actividad2.id)

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
        actividad_vacia = self.session.query(Actividad).filter( Actividad.nombre == "" ).first()
        self.assertEqual(actividad_vacia, None) #No pueden existir actividades vacias

        self.control_cuenta.crearActividad("integracion")
        actividad_con_nombre = self.session.query(Actividad).filter( Actividad.nombre == "integracion").first()
        self.assertNotEqual(actividad_con_nombre, None)
        nombre_actividad = actividad_con_nombre.nombre
        self.assertEqual(nombre_actividad, "integracion")

        with self.assertRaises(IntegrityError):
            self.assertRaises(self.control_cuenta.crearActividad("integracion"))
    
    def test_asociar_viajero_a_actividad(self):
        self.assertEqual(None, self.control_cuenta.asociarViajeroAActividad())
        
