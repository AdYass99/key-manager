"""
This module initializes the Flask application and registers the blueprints for the different routes.
It also sets up the database connection and configuration settings.
"""

import os

from flask import Flask

from app.db.database import init_db
from app.routes.authentication import autentification_bp
from app.routes.main import home
from app.routes.passwords import passwords_bp


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
