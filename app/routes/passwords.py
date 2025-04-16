from flask import request, Blueprint, render_template, redirect, url_for , session
from app.database import query_get, query_set
from app.routes.criptography import encrypt, decrypt
import pyperclip
import random
import string

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/add', methods=['POST'])
def add():
    username = request.form['username']
    password = request.form['password']
    master_password = session.get('master_password')
    encrypted_password = encrypt(password, master_password)
    query_set(f"INSERT INTO users (username, password,salt,nonce,tag) VALUES ("   +
              f"'{username}', " +
              f"'{encrypted_password['cipher_text']}',"   +
              f"'{encrypted_password['salt']}',"  +
              f"'{encrypted_password['nonce']}'," +
              f"'{encrypted_password['tag']}'"   +
              ")")
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/view', methods=['GET'])
def view():
    user_id = request.args.get('filter') 
    if user_id:
        data = query_get(f"SELECT id, username, password FROM users WHERE username like '%{user_id}%'")
    else:
        data = query_get(f"SELECT id, username, password FROM users")
    return render_template('search.html', data=data)

@passwords_bp.route('/copy', methods=['GET'])
def copy():
    user_id = request.args.get('user_id') 
    master_password = session.get('master_password')
    data = query_get(f"SELECT password,salt,nonce,tag FROM users WHERE Id = {user_id}")
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
def config():
    data = query_get("SELECT id, username, password FROM users")
    return render_template('config.html', data=data)

@passwords_bp.route('/delete', methods=['POST'])
def delete():
    user_id = request.form.get('user_id') 
    query_set(f"DELETE FROM users WHERE id = {user_id}")
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/generate', methods=['GET'])
def generate():
    generated_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    data = query_get("SELECT id, username, password FROM users")
    return render_template('config.html',data=data, generated_password=generated_password)