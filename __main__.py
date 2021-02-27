import sys
from PyQt5.QtWidgets import QApplication
from src.vista.Interfaz_CuentasClaras import App_CuentasClaras
from src.logica.Logica_mock import Logica_mock
from src.logica.control_cuenta import ControlCuenta

if __name__ == '__main__':
    #Punto inicial de la aplicación 


    control_cuenta = ControlCuenta()
    
    logica = Logica_mock()

    app = App_CuentasClaras(sys.argv, logica)
    sys.exit(app.exec_())