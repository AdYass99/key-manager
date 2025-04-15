from flask import request, Blueprint, render_template, redirect, url_for , session
from app.database import query_get, query_set
import pyperclip

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/add', methods=['POST'])
def add():
    username = request.form['username']
    password = request.form['password']
    query_set(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/view', methods=['GET'])
def view():
    data = query_get(f"SELECT id, username, password FROM users")
    return render_template('search.html', data=data)

@passwords_bp.route('/view/<string:user_id>', methods=['GET'])
def search(user_id):
    data = query_get(f"SELECT id,username, password FROM users WHERE username LIKE '%{user_id}%'")
    return render_template('search.html', data=data)

@passwords_bp.route('/copy/<int:user_id>', methods=['GET'])
def copy(user_id):
    data = query_get(f"SELECT password FROM users WHERE Id = {user_id}")
    pyperclip.copy(data[0][0])
    return redirect(request.referrer)

@passwords_bp.route('/config', methods=['GET'])
def config():
    data = query_get("SELECT id, username, password FROM users")
    return render_template('config.html', data=data)

@passwords_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    query_set(f"DELETE FROM users WHERE id = {user_id}")
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '1234':
            session['logged_in'] = True
            return redirect(url_for('passwords.view'))
        else:
            return render_template('index.html', error="Contraseña incorrecta")
    return render_template('index.html')