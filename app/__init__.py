from flask import Flask
from .database import init_db
from .routes.passwords import passwords_bp
from .routes.autentification import autentification_bp
from .routes.home import home
import os

def create_app():
    app = Flask(__name__)
    app.config['DATABASE_PATH'] = os.path.join('instance','passwords.db')
    app.config['SECRET_KEY'] = 'tfg_uoc_key_manager'
    app.register_blueprint(passwords_bp)
    app.register_blueprint(autentification_bp)    
    app.add_url_rule('/', 'home', home)
    app.secret_key = 'uoc'  # Cambia esto por una clave secreta segura

    with app.app_context():
        init_db()
    return app