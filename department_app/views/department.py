"""
Department views module.
"""
from flask import render_template

from department_app.forms.forms import AddDepartmentForm
from department_app.views import views_bp


@views_bp.route('/departments')
def departments():
    """
    Handles requests to the /departments route
    """
    return render_template('departments.html')


@views_bp.route('/add_department')
def add_department():
    """
    Handles requests to the /add_department route
    """
    form = AddDepartmentForm()
    title = 'New Department'
    return render_template('add_department.html', form=form, title=title)


@views_bp.route('/edit_department/<uuid>')
def edit_department(uuid):
    """
    Handles requests to the /edit_department/<uuid> route
    """
    form = AddDepartmentForm()
    title = 'Edit Department'
    return render_template('edit_department.html', form=form, uuid=uuid, title=title)
