from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date  # Importar para trabajar con fechas
from models.database_setup import db, Usuario
from models.database_setup import Asistencia

# Asegúrate de que este modelo esté bien definido

# Configuración de la aplicación y SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Deshabilitar la advertencia de modificaciones de SQLAlchemy
db.init_app(app)
socketio = SocketIO(app)

# Inicializando Flask-Migrate
migrate = Migrate(app, db)

# Configurar el manejo de sesiones de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Especificamos la vista para el login


# Definir la función user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Inicializar la base de datos
def init_db():
    with app.app_context():
        db.create_all()


# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        rol = request.form['rol']

        # Verificar si el correo ya está registrado
        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            flash('El correo ya está registrado. Intenta con otro.', 'danger')
            return redirect(url_for('registro'))

        # Validación de contraseña
        if len(contrasena) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return redirect(url_for('registro'))

        # Cifrado de la contraseña
        contrasena_cifrada = generate_password_hash(contrasena)

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre,
                                correo=correo,
                                contrasena=contrasena_cifrada,
                                rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')


# Ruta para el inicio de sesión de usuarios
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['username']
        contrasena = request.form['password']

        # Verificar si el usuario existe
        usuario = Usuario.query.filter_by(correo=correo).first()

        if not usuario:
            flash('Usuario no registrado', 'danger')
            return redirect(
                url_for('login'))  # Redirige al login si no existe el usuario

        # Verificar si la contraseña es correcta utilizando check_password_hash
        if not check_password_hash(usuario.contrasena, contrasena):
            flash('Contraseña incorrecta', 'danger')
            return redirect(url_for(
                'login'))  # Redirige al login si la contraseña es incorrecta

        # Iniciar sesión con el usuario
        login_user(usuario)
        flash('Inicio de sesión exitoso', 'success')

        # Redirigir al dashboard correspondiente según el rol
        if usuario.rol == 'estudiante':
            return redirect(url_for('dashboard_estudiante'))
        elif usuario.rol == 'profesor':
            return redirect(url_for('profesor_dashboard'))

    return render_template('login.html')


# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))


# Dashboard para estudiantes
@app.route('/dashboard/estudiante')
@login_required
def dashboard_estudiante():
    # Aquí puedes agregar lógica dinámica para mostrar la información relevante
    return render_template('dashboard_estudiante.html')


# Dashboard para profesores
@app.route('/profesor_dashboard', methods=['GET', 'POST'])
@login_required
def profesor_dashboard():
    if request.method == 'POST':
        # Registrar la asistencia manual
        usuario_id = request.form['usuario_id']
        estado = request.form['estado']

        if usuario_id and estado:
            estudiante = Usuario.query.get(usuario_id)
            if estudiante:
                asistencia = Asistencia(usuario_id=estudiante.id,
                                        fecha=date.today(),
                                        presente=(estado == 'presente'))
                db.session.add(asistencia)
                db.session.commit()
                flash('Asistencia registrada correctamente', 'success')
            else:
                flash('Estudiante no encontrado', 'danger')

    # Obtener todos los estudiantes para mostrarlos en el formulario
    estudiantes = Usuario.query.filter_by(rol='estudiante').all()
    return render_template('profesor_dashboard.html', estudiantes=estudiantes)


# Ruta de chat usando SocketIO
@socketio.on('message')
def handle_message(msg):
    print('Mensaje recibido: ' + msg)
    socketio.send(msg, broadcast=True)


# Inicia la aplicación
if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000)
