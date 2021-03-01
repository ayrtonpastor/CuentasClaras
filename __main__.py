import sys
from PyQt5.QtWidgets import QApplication
from src.vista.Interfaz_CuentasClaras import App_CuentasClaras
from src.logica.control_cuenta import ControlCuenta
from src.mockdata.mockdata import MockDataFactory   

if __name__ == '__main__':
    #Punto inicial de la aplicación 

    control_cuenta = ControlCuenta()

    factory_mockup_data = MockDataFactory()
    factory_mockup_data.setUp()
    
    try:
        app = App_CuentasClaras(sys.argv, control_cuenta)
        sys.exit(app.exec_())
    finally:
        factory_mockup_data.tearDown()
        
