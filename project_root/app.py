from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importar Flask-Migrate
from config import Config

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Crear la instancia de la base de datos
db = SQLAlchemy(app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)


# Definir rutas
@app.route('/')
def home():
    # Si el usuario ya está autenticado, redirige al dashboard correspondiente
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    from models.user import User  # Mover la importación aquí
    if request.method == 'POST':
        # Aquí procesamos el inicio de sesión
        username = request.form['username']
        password = request.form['password']

        # Buscar al usuario por su nombre de usuario
        user = User.query.filter_by(username=username).first()

        if user:
            # Si el usuario existe, verificamos la contraseña
            if user.check_password(password):
                session['user_id'] = user.id
                flash('Inicio de sesión exitoso', 'success')
                if user.role == 'professor':
                    return redirect(url_for('professor_dashboard'))  # Redirige a panel del profesor
                else:
                    return redirect(url_for('student_dashboard'))  # Redirige a panel del estudiante
            else:
                flash('Contraseña incorrecta', 'danger')  # Si la contraseña es incorrecta
        else:
            flash('Usuario no registrado. Por favor, regístrate.', 'warning')  # Si el usuario no existe

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    from models.user import User  # Mover la importación aquí
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder al dashboard', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.role == 'professor':
        return redirect(url_for('professor_dashboard'))  # Panel del profesor
    else:
        return redirect(url_for('student_dashboard'))  # Panel del estudiante


@app.route('/professor_dashboard')
def professor_dashboard():
    from models.user import User  # Mover la importación aquí
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder al dashboard', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.role == 'professor':
        return render_template('dashboard.html', user=user,
                               role='professor')  # Dashboard del profesor
    else:
        flash('Acceso denegado', 'danger')
        return redirect(url_for('login'))


@app.route('/student_dashboard')
def student_dashboard():
    from models.user import User  # Mover la importación aquí
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder al dashboard', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.role == 'student':
        return render_template('student_dashboard.html',
                               user=user,
                               role='student')  # Dashboard del estudiante
    else:
        flash('Acceso denegado', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('home'))


# Configuración para iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
