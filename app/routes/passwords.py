from flask import request, Blueprint, render_template, redirect, url_for , session
from app.database import query_get, query_set

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/add', methods=['POST'])
def add_password():
    username = request.form['username']
    password = request.form['password']
    query_set(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    return redirect(url_for('passwords.config'))

@passwords_bp.route('/view', methods=['GET'])
def search_password():
    query = request.args.get('query', '')
    data = query_get("SELECT username, password FROM users WHERE username LIKE '%{query}%'")
    return render_template('search.html', data=data, query=query)

@passwords_bp.route('/config', methods=['GET'])
def config():
    data = query_get("SELECT id, username, password FROM users")
    return render_template('config.html', data=data)

@passwords_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_password(user_id):
    query_set(f"DELETE FROM users WHERE id = {user_id}")
    return redirect(url_for('passwords.config'))


@passwords_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '1234':
            session['logged_in'] = True
            return redirect(url_for('passwords.config'))
        else:
            return render_template('index.html', error="Contraseña incorrecta")
    return render_template('index.html')