import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_llave_secreta_segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Puedes cambiar esto si usas otra base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
