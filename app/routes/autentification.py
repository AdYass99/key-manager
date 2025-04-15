from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import request, Blueprint, render_template, redirect, url_for , session


autentification_bp = Blueprint('autentification', __name__)
ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)

master_password = '1234'
master_password_hash = ph.hash(master_password)

def verify_master_key(password, hashed_password):
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False
    
    
@autentification_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if verify_master_key(password, master_password_hash):
            session['logged_in'] = True
            return redirect(url_for('passwords.view'))
        else:
            return render_template('index.html', error="Contraseña incorrecta")
    return render_template('index.html')