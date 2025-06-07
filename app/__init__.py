"""
This module initializes the Flask application and registers the blueprints for the different routes.
It also sets up the database connection and configuration settings.
"""

import os

from flask import Flask, session
from flask_talisman import Talisman

from app.db.database import init_db
from app.routes.authentication import autentification_bp
from app.routes.main import home
from app.routes.passwords import passwords_bp


def create_app():
    app = Flask(__name__)
    app.config['DATABASE_PATH'] = os.path.join('instance','passwords.db')
    app.config['SECRET_KEY'] = 'tfg_uoc_key_manager'
    # Configurar cookies seguras
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    # Activar protección CSP + HSTS + X-Frame-Options
    Talisman(
        app,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline'",
            'connect-src': "'self'",
            'img-src': "'self' data:",
            'style-src': "'self'"
        },
        force_https=True,
        frame_options='DENY'
    )

    # Registrar blueprints
    
    app.register_blueprint(passwords_bp)
    app.register_blueprint(autentification_bp)
    app.add_url_rule('/', 'home', home)
    app.secret_key = 'uoc'

    @app.context_processor
    def inject_user():
        return {'logged_in_user': session.get('username')}

    with app.app_context():
        init_db()
    return app
