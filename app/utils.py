"""
Utility functions for the application.
This module contains helper functions for user authentication and session management.
"""

from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para continuar', 'error')
            return redirect(url_for('autentification.login'))
        return f(*args, **kwargs)
    return decorated_function
