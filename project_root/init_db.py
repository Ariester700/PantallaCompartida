from app import db
from models.user import User

# Inicializar la base de datos
with app.app_context():
    db.create_all()

    # Crear usuarios de prueba si no existen
    if not User.query.filter_by(username='profesor').first():
        profesor = User(username='profesor',
                        password='profesor123',
                        role='professor')
        db.session.add(profesor)

    if not User.query.filter_by(username='estudiante').first():
        estudiante = User(username='estudiante',
                          password='estudiante123',
                          role='student')
        db.session.add(estudiante)

    db.session.commit()
