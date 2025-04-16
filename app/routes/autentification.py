from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import request, Blueprint, render_template, redirect, url_for , session
from flask import current_app
import json
import hmac
import hashlib
import os

autentification_bp = Blueprint('autentification', __name__)
ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)

FILE_PATH=os.path.join('instance','master_password.json')

def verify_master_key(password):
    try:
        hashed_password=load_master_password_hash()
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False
 
def save_master_password_hash(hash_value):
    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    # Crear un HMAC para verificar la integridad del archivo
    SECRET_KEY = current_app.config['SECRET_KEY'].encode('utf-8')
    hmac_value = hmac.new(SECRET_KEY, hash_value.encode(), hashlib.sha256).hexdigest()
    data = {
        'master_password_hash': hash_value,
        'hmac': hmac_value
    }
    # Guardar en un archivo JSON
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
        
def load_master_password_hash():
    try:
        with open(FILE_PATH, 'r') as file:
            data = json.load(file)
            hash_value = data['master_password_hash']
            hmac_value = data['hmac']
            # Verificar la integridad del archivo
            SECRET_KEY = current_app.config['SECRET_KEY'].encode('utf-8')
            expected_hmac = hmac.new(SECRET_KEY, hash_value.encode(), hashlib.sha256).hexdigest()
            if hmac_value != expected_hmac:
                raise ValueError("El archivo ha sido modificado manualmente o está corrupto.")
            return hash_value
    except FileNotFoundError:
        raise FileNotFoundError("El archivo de configuración no existe.")
    except KeyError:
        raise ValueError("El archivo de configuración no tiene el formato esperado.")
     
@autentification_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if os.path.exists(FILE_PATH):         
            password = request.form['password']
            if verify_master_key(password):
                session['logged_in'] = True
                session['master_password'] = password
                return redirect(url_for('passwords.view'))          
            else:
                return render_template('index.html', error="Contraseña incorrecta")
        else:
            password = request.form['password']
            hashed_password = ph.hash(password)
            # Guardar el hash de la contraseña maestra en un archivo JSON
            save_master_password_hash(hashed_password)
            session['logged_in'] = True
            session['master_password'] = password
            return redirect(url_for('passwords.view'))
    return render_template('index.html')