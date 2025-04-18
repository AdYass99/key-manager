"""
This module contains the routes for managing passwords in the application.
It includes routes for adding, viewing, copying, deleting, and generating passwords.
"""

import random
import string

from flask import (Blueprint, jsonify, redirect, render_template, request, session,
                   url_for)

from app.db.database import query_get, query_set
from app.securtiy.criptography import decrypt, encrypt
from app.routes.authentication import login_required

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

@passwords_bp.route('/config', methods=['GET'])
@login_required
def config():
    user_id = session['user_id']
    data = query_get(f"SELECT id, account_name, password FROM passwords WHERE user_id = {user_id}")
    return render_template('config.html', data=data)

@passwords_bp.route('/delete', methods=['POST'])
@login_required
def delete():
    password_id = request.form.get('password_id')
    query_set(f"DELETE FROM passwords WHERE id = {password_id}")
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/generate', methods=['GET'])
@login_required
def generate():
    generated_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    data = query_get("SELECT id, account_name, password FROM passwords")
    return render_template('config.html',data=data, generated_password=generated_password)

@passwords_bp.route('/decrypt', methods=['POST'])
@login_required
def decrypt_password():
    password_id = request.json.get('password_id')
    master_password = session.get('master_password')

    # Obtener la contraseña cifrada de la base de datos
    data = query_get(f"SELECT password, salt, nonce, tag FROM passwords WHERE id = {password_id}")
    if not data:
        return jsonify({'error': 'Contraseña no encontrada'}), 404

    encrypted_password = {
        'cipher_text': data[0][0],
        'salt': data[0][1],
        'nonce': data[0][2],
        'tag': data[0][3]
    }

    try:
        # Desencriptar la contraseña
        decrypted_password = decrypt(encrypted_password, master_password)
        return jsonify({'password': decrypted_password})
    except Exception as e:
        return jsonify({'error': 'Error al desencriptar la contraseña:'}), 500
