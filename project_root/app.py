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

print(app.url_map)

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


# Ruta principal (Home)
@app.route('/')
def home():
    return "<h1>Página de inicio</h1><p>Flask está funcionando correctamente.</p>"


# Ruta de prueba
@app.route('/test')
def test():
    return "<h1>Página de prueba</h1><p>Esta es una página de prueba para verificar las rutas.</p>"


# Ruta de inicio (login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validación de usuario
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('login.html')


# Ruta del dashboard
@app.route('/dashboard')
def dashboard():
    return "<h1>Bienvenido al Dashboard</h1>"


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0')  # Aseguramos que Flask escuche en todas las interfaces
