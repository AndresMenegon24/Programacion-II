from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Caso(db.Model):
    __tablename__ = 'casos'
    
    dni = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.Enum('M', 'F'), nullable=False)
    calle = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    barrio = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    grupo = db.Column(db.Enum('A', 'B', 'C'), nullable=False)
    ingresa_con_vida = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    @staticmethod
    def calcular_edad(fecha_nacimiento):
        today = date.today()
        return today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    def to_dict(self):
        return {
            'dni': self.dni,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento,
            'edad': self.edad,
            'sexo': self.sexo,
            'calle': self.calle,
            'numero': self.numero,
            'barrio': self.barrio,
            'localidad': self.localidad,
            'departamento': self.departamento,
            'codigo_postal': self.codigo_postal,
            'telefono': self.telefono,
            'correo': self.correo,
            'grupo': self.grupo,
            'ingresa_con_vida': self.ingresa_con_vida,
            'timestamp': self.timestamp
        }
