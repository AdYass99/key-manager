from flask import Flask
from .database import init_db
from .routes.passwords import passwords_bp
from .routes.home import home

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'instance/passwords.db'


    init_db()

    app.register_blueprint(passwords_bp)
    app.add_url_rule('/', 'home', home)
    app.secret_key = '1234'  # Cambia esto por una clave secreta segura

    return app