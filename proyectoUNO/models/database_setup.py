from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # Importar UserMixin de Flask-Login

app = Flask(__name__)

# Configuración de la base de datos
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Usando SQLite como base de datos
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para evitar advertencias
app.config[
    'SECRET_KEY'] = 'mi_secreto'  # Necesario para sesiones de Flask-Login

# Inicializando SQLAlchemy
db = SQLAlchemy(app)


class Usuario(db.Model, UserMixin):  # Heredar de UserMixin
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('profesor', 'estudiante', name='roles_enum'),
                    nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP,
                               default=db.func.current_timestamp())
    activo = db.Column(db.Boolean, default=True)  # Agregar campo 'activo'

    # Relaciones
    asistencia = db.relationship('Asistencia', backref='usuario_asistencia', lazy=True)
    trabajos = db.relationship('Trabajo', backref='usuario', lazy=True)
    resultados = db.relationship('Resultado', backref='usuario', lazy=True)

    def is_active(self):
        """Método que define si el usuario está activo"""
        return self.activo  # Devuelve el valor del campo 'activo'


class Asistencia(db.Model):
    __tablename__ = 'Asistencia'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False)

    usuario = db.relationship('Usuario', backref='asistencia_usuario')  # Cambié el backref


class Trabajo(db.Model):
    __tablename__ = 'Trabajos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_subida = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    archivo_url = db.Column(db.String(255))


class Examen(db.Model):
    __tablename__ = 'Examenes'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)  # Duración en minutos
    materia = db.Column(db.String(255), nullable=False)


class Resultado(db.Model):
    __tablename__ = 'Resultados'
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('Examenes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    puntuacion = db.Column(db.Numeric(5, 2), nullable=False)
    fecha_realizado = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())


class RestriccionModoExamen(db.Model):
    __tablename__ = 'RestriccionesModoExamen'
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('Examenes.id'), nullable=False)
    restriccion = db.Column(db.String(255), nullable=False)


# Crear la base de datos (si no existe)
def init_db(app):
    with app.app_context():
        db.create_all()  # Crea todas las tablas si no existen


if __name__ == "__main__":
    init_db(app)  # Pasar el objeto app para crear las tablas si no existen
    app.run(debug=True)

