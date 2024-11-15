# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_clave_secreta'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
