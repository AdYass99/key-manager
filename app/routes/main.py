"""
Home route for the application.
This module defines the home route for the application using Flask's Blueprint feature.
"""

from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html')
