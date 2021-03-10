from PyQt5.QtWidgets import QApplication, QMessageBox
from .Vista_lista_actividades import Vista_lista_actividades
from .Vista_lista_viajeros import Vista_lista_viajeros
from .Vista_actividad import Vista_actividad
from .Vista_reporte_compensacion import Vista_reporte_compensacion
from .Vista_reporte_gastos import Vista_reporte_gastos_viajero

class App_CuentasClaras(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_CuentasClaras, self).__init__(sys_argv)

        self.logica = logica
        self.mostrar_vista_lista_actividades()


    def mostrar_vista_lista_actividades(self):
        """
        Esta función inicializa la ventana de la lista de actividades
        """
        self.vista_lista_actividades = Vista_lista_actividades(self)
        self.vista_lista_actividades.mostrar_actividades(self.logica.listarActividades())


    def insertar_actividad(self, nombre):
        """
        Esta función inserta una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        try:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al crear actividad")

            if not nombre:
                raise ValueError("El nombre no puede ser vacio")

            self.logica.crearActividad(nombre)
            self.vista_lista_actividades.mostrar_actividades(self.logica.listarActividades())
        except ValueError as e:
            mensaje_error.setText("El nombre de la actividad no puede ser vacio.")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        except Exception as e:
            mensaje_error.setText("El nombre de la actividad está repetido.")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
            

            


    def editar_actividad(self, indice_actividad, nombre):
        """
        Esta función editar una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.actividades[indice_actividad] = nombre
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)

    def eliminar_actividad(self, indice_actividad):
        """
        Esta función elimina una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.actividades.pop(indice_actividad)
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)


    def mostrar_viajeros(self):
        """
        Esta función muestra la ventana de la lista de viajeros
        """
        self.vista_lista_viajeros = Vista_lista_viajeros(self)
        self.vista_lista_viajeros.mostrar_viajeros(self.dar_viajeros())

    def insertar_viajero(self, nombre, apellido):
        """
        Esta función inserta un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        crear_viajero = self.logica.crearViajero(nombre, apellido)
        if crear_viajero is False:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar los cambios")
            if nombre is None or nombre == "" or apellido is None or apellido == "":
                mensaje_error.setText("El nombre y el apellido no deben estar en blanco.")
            else:
                mensaje_error.setText("Ya existe un viajero con estos datos.")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()

        self.vista_lista_viajeros.mostrar_viajeros(self.dar_viajeros())

    def editar_viajero(self, viajero, nombre, apellido):
        """
        Esta función edita un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        editar_viajero = self.logica.editarViajero(viajero.id, nombre, apellido)
        if not editar_viajero:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar los cambios")
            if nombre is None or nombre == "" or apellido is None or apellido == "":
                mensaje_error.setText("El nombre y el apellido no deben estar en blanco.")
            else:
                mensaje_error.setText("Ya existe un viajero con estos datos.")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()

        self.vista_lista_viajeros.mostrar_viajeros(self.dar_viajeros())

    def eliminar_viajero(self, indice_viajero):
        """
        Esta función elimina un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros.pop(indice_viajero)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def mostrar_actividad(self, actividad = None):
        """
        Esta función muestra la ventana detallada de una actividad
        """
        if actividad == None:
            raise Exception("Actividad nula")
        self.vista_actividad = Vista_actividad(self)
        self.vista_actividad.mostrar_gastos_por_actividad(actividad, self.logica.listarGastos(actividad.id))

    def insertar_gasto(self, concepto, fecha, valor, viajero_nombre, viajero_apellido):
        """
        Esta función inserta un gasto a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.append({"Concepto":concepto, "Fecha": fecha, "Valor": int(valor), "Nombre": viajero_nombre, "Apellido": viajero_apellido})
        self.vista_actividad.mostrar_gastos_por_actividad(self.logica.actividades[self.actividad_actual], self.logica.gastos)

    def editar_gasto(self, indice, concepto, fecha, valor, viajero_nombre, viajero_apellido):
        """
        Esta función edita un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos[indice] = {"Concepto":concepto, "Fecha": fecha, "Valor": int(valor), "Nombre": viajero_nombre, "Apellido": viajero_apellido}
        self.vista_actividad.mostrar_gastos_por_actividad(self.logica.actividades[self.actividad_actual], self.logica.gastos)

    def eliminar_gasto(self, indice):
        """
        Esta función elimina un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.pop(indice)
        self.vista_actividad.mostrar_gastos_por_actividad(self.logica.actividades[self.actividad_actual], self.logica.gastos)

    def mostrar_reporte_compensacion(self, actividad):
        """
        Esta función muestra la ventana del reporte de compensación
        """
        self.vista_reporte_comensacion = Vista_reporte_compensacion(self)
        self.vista_reporte_comensacion.mostrar_reporte_compensacion(matriz_compensacion=self.logica.crearReporteCompensacion(actividad.id), actividad=actividad)

    def mostrar_reporte_gastos_viajero(self, actividad):
        """
        Esta función muestra el reporte de gastos consolidados
        """
        self.vista_reporte_gastos = Vista_reporte_gastos_viajero(self)
        self.vista_reporte_gastos.mostar_reporte_gastos(lista_gastos=self.logica.crearReporteGastosPorViajero(actividad.id), actividad=actividad)

    def actualizar_viajeros(self, n_viajeros_en_actividad):
        """
        Esta función añade un viajero a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros_en_actividad = n_viajeros_en_actividad

    def dar_viajeros(self):
        """
        Esta función pasa la lista de viajeros (debe implementarse como una lista de diccionarios o str)
        """
        return self.logica.listarViajeros()

    def dar_viajeros_en_actividad(self):
        """
        Esta función pasa los viajeros de una actividad (debe implementarse como una lista de diccionarios o str)
        """
        return self.logica.viajeros_en_actividad

    def terminar_actividad(self, indice):
        """
        Esta función permite terminar una actividad (debe implementarse)
        """
        pass
