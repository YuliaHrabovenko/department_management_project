"""
Home view module.
"""

from flask import render_template
from department_app.views import views_bp


@views_bp.route('/')
def home():
    """
    Handles requests to the / route
    """
    return render_template('home.html')
