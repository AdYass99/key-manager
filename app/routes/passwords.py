from flask import request, Blueprint, render_template, redirect, url_for , session
from app.database import query_get, query_set
from app.routes.criptography import encrypt, decrypt
from app.utils import login_required
import pyperclip
import random
import string

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/add', methods=['POST'])
@login_required
def add():
    account_name = request.form['account_name']
    password = request.form['password']
    user_id = session['user_id']
    master_password = session.get('master_password')
    encrypted_password = encrypt(password, master_password)
    query_set(f"""
        INSERT INTO passwords (user_id, account_name, password, salt, nonce, tag)
        VALUES (
            {user_id},
            '{account_name}',
            '{encrypted_password['cipher_text']}',
            '{encrypted_password['salt']}',
            '{encrypted_password['nonce']}',
            '{encrypted_password['tag']}'
        )
    """)
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/view', methods=['GET'])
@login_required
def view():
    user_id = session['user_id']
    account_name = request.args.get('filter') 
    
    if account_name:
        data = query_get(f"""
                    SELECT id, account_name, password 
                    FROM passwords 
                    WHERE 
                        user_id = {user_id} And
                        account_name like '%{account_name}%'
                    """) 
    else:
        data = query_get(f"""
                    SELECT id, account_name, password 
                    FROM passwords 
                    WHERE 
                    user_id = {user_id}
                """)
    return render_template('search.html', data=data)

@passwords_bp.route('/copy', methods=['GET'])
@login_required
def copy():
    password_id = request.args.get('password_id') 
    master_password = session.get('master_password')
    data = query_get(f"SELECT password,salt,nonce,tag FROM passwords WHERE Id = {password_id}")
    encrypted_password = {
        'cipher_text': data[0][0],
        'salt': data[0][1],
        'nonce': data[0][2],
        'tag': data[0][3]
    }
    decrypted_password = decrypt(encrypted_password, master_password)
    pyperclip.copy(decrypted_password)
    return redirect(request.referrer)

@passwords_bp.route('/config', methods=['GET'])
@login_required
def config():
    user_id = session['user_id']
    data = query_get(f"SELECT id, account_name, password FROM passwords WHERE user_id = {user_id}")
    return render_template('config.html', data=data)

@passwords_bp.route('/delete', methods=['POST'])
@login_required
def delete():
    password_id = request.form.get('password_id') ##TODO: cambiar a id de la tabla password
    query_set(f"DELETE FROM passwords WHERE id = {password_id}")
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/generate', methods=['GET'])
@login_required
def generate():
    generated_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    data = query_get("SELECT id, account_name, password FROM passwords")
    return render_template('config.html',data=data, generated_password=generated_password)