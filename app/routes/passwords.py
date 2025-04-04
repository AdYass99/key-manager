from flask import request, Blueprint
from app.database import query_get, query_set

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/add', methods=['POST'])
def add_password():
    username = request.form['username']
    password = request.form['password']
    
    query_set(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    
    return "Contraseña almacenada! <a href='/'>Volver</a>"

@passwords_bp.route('/view')
def view_passwords():
    data = query_get("SELECT username, password FROM users")
    
    return '<br>'.join([f"Usuario: {row[0]}, Contraseña: {row[1]}" for row in data])