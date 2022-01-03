"""
Employee views module.
"""

from flask import render_template

from department_app.forms.forms import AddEmployeeForm, DateEmployeeForm
from department_app.views import views_bp


@views_bp.route('/employees')
def employees():
    """
    Handles requests to the /employees route
    """
    form = DateEmployeeForm()
    return render_template('employees.html', form=form)


@views_bp.route('/edit_employee/<uuid>')
def edit_employee(uuid):
    """
    Handles requests to the /edit_employee/<uuid> route
    """
    form = AddEmployeeForm()
    title = 'Edit Employee'
    return render_template('edit_employee.html', title=title, uuid=uuid, form=form)


@views_bp.route('/add_employee')
def add_employee():
    """
    Handles requests to the /add_employee route
    """
    form = AddEmployeeForm()
    title = 'New Employee'
    return render_template('add_employee.html', title=title, form=form)
