from src.modelo.declarative_base import engine, Base, session

class ControlCuenta():

    def __init__(self):
        Base.metadata.create_all(engine)
    
    def listarActividades(self):
        pass
    
    def crearReporteCompensacion(self, actividad_id):
        pass
    
    def listarGastos(self, actividad_id):
        pass
