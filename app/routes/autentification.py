from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import flash, request, Blueprint, render_template, redirect, url_for , session
from app.database import query_get, query_set
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import json
import hmac
import hashlib
import os

autentification_bp = Blueprint('autentification', __name__)
   
@autentification_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form['password']
        user = query_get(f"SELECT id, master_password_hash FROM users WHERE username = '{username}'")
        if user and check_password_hash(user[0][1], password):
            session['user_id'] = user[0][0] 
            session['username'] = username
            session['master_password'] = password
            return redirect(url_for('passwords.view'))
        else:
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
            hashed_password = generate_password_hash(password)
            query_set(f"INSERT INTO users (username, master_password_hash) VALUES ('{username}', '{hashed_password}')")
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('autentification.login'))

    return render_template('register.html')