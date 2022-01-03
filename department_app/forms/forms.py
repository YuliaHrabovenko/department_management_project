"""
Forms module for storing form classes:
 - AddEmployeeForm to add or edit an employee
 - AddDepartmentForm to add or edit a department
 - DateEmployeeForm to search for employees by date or period between dates
"""
import operator
from functools import partial

from sqlalchemy import orm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField


from department_app.models.department import DepartmentModel


def get_department(columns=None):
    """
    Specify the columns needed for query using a DepartmentModel model
    """
    department = DepartmentModel.query
    if columns:
        department = department.options(orm.load_only(*columns))
    return department


def get_department_factory(columns=None):
    """
    Receive departments names from query using uuid and name columns
    """
    return partial(get_department, columns=columns)


class AddEmployeeForm(FlaskForm):
    """
    Form for employee addition.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=25)])
    birth_date = DateField('Birth date', format='%y-%m-%d', validators=[DataRequired()])
    department = QuerySelectField(query_factory=get_department_factory(['uuid', 'name']),
                                  get_label='name', get_pk=operator.attrgetter("uuid"))
    salary = IntegerField('Salary')
    submit = SubmitField('Submit')


class AddDepartmentForm(FlaskForm):
    """
    Form for department addition.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=120)])
    submit = SubmitField('Submit')


class DateEmployeeForm(FlaskForm):
    """
    Form for search of employees by date or in periods of dates.
    """
    start_date = DateField('Start date', format='%y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End date', format='%y-%m-%d', validators=[DataRequired()])
    check_box = BooleanField('Search by certain date', default=False)
    submit = SubmitField('Search')
