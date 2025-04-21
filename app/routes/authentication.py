"""
    Autentification routes for the application.
    This module contains the routes for user login, logout, and registration.
    It uses Flask's Blueprint to organize the routes and handle user sessions.
"""

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from functools import wraps

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from datetime import datetime, timedelta

from app.db.database import query_get, query_set

autentification_bp = Blueprint('autentification', __name__)
ph = PasswordHasher(time_cost=4, memory_cost=256000, parallelism=4)

failed_attempts = {}
max_attempts = 5
lockout_time = timedelta(minutes=15)

@autentification_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form['password']
        ip_address = request.remote_addr
          # Verificar intentos fallidos
        if ip_address in failed_attempts:
            attempts, last_attempt = failed_attempts[ip_address]
            if attempts >= max_attempts and datetime.now() - last_attempt < lockout_time:
                flash('Demasiados intentos fallidos. Intenta nuevamente más tarde.', 'error')
                return render_template('index.html')

        user = query_get(f"SELECT id, master_password_hash FROM users WHERE username = '{username}'")
        if user :
            # Verificar la contraseña usando Argon2
            try:
                ph.verify(user[0][1], password)
                session['user_id'] = user[0][0]
                session['username'] = username
                session['master_password'] = password
                if ip_address in failed_attempts:
                    del failed_attempts[ip_address]  # Restablecer intentos fallidos
                return redirect(url_for('passwords.view'))
            except VerifyMismatchError:
                pass
        
        # Registrar intento fallido
        if ip_address not in failed_attempts:
            failed_attempts[ip_address] = (1, datetime.now())
        else:
            attempts, _ = failed_attempts[ip_address]
            failed_attempts[ip_address] = (attempts + 1, datetime.now())
        
        flash('Usuario o contraseña incorrectos', 'error')
    return render_template('index.html')

@autentification_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('autentification.login'))

@autentification_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar si el usuario ya existe
        existing_user = query_get(f"SELECT id FROM users WHERE username = '{username}'")
        if existing_user:
            flash('El usuario ya existe', 'error')
        else:
            # Guardar el nuevo usuario con la contraseña hasheada
            hashed_password = ph.hash(password)
            query_set(f"""
                INSERT INTO users (username, master_password_hash)
                      VALUES ('{username}', '{hashed_password}')
                      """)
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('autentification.login'))

    return render_template('register.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para continuar', 'error')
            return redirect(url_for('autentification.login'))
        return f(*args, **kwargs)
    return decorated_function
