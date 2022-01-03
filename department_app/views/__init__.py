"""
Module __init__.py.
"""
from flask import Blueprint
views_bp = Blueprint('views_bp', __name__)

from department_app.views.department import departments, add_department, edit_department
from department_app.views.employee import employees, add_employee, edit_employee
from department_app.views.home import home
