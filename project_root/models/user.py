from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inicialización de la aplicación
app = Flask(__name__)
app.config[
    'SECRET_KEY'] = 'clave-secreta'  # Cambiar a una clave segura en producción
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Configuración de la base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)


# Modelo de base de datos para el usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50),
                     nullable=False)  # Puede ser 'profesor' o 'estudiante'

    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(
            password)  # Contraseña encriptada
        self.role = role


# Crear la base de datos si no existe
with app.app_context():
    db.create_all()
