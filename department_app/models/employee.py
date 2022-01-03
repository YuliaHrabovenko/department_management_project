"""
This module defines the following classes:
- EmployeeModel, employee model used to represent employees
"""
from datetime import date
import uuid
from department_app.extensions import db

# pylint: disable=too-few-public-methods


class EmployeeModel(db.Model):
    """
    The EmployeeModel object represents employee table in db.
    """

    # name of the department table in db
    __tablename__ = 'employee'

    # id of the employee in db
    id = db.Column(db.Integer, primary_key=True)
    # employee name column in db
    name = db.Column(db.String(25), nullable=False)
    # birth_date of employee column
    birth_date = db.Column(db.DateTime, nullable=False)
    # salary of employee column
    salary = db.Column(db.Integer, nullable=False)
    # employee uuid column
    uuid = db.Column(db.String(36), unique=True)
    # database id of the department employee works in (foreign key)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, birth_date, salary, department=None):
        """
        Constructor of EmployeeModel class.
        :param name: employee name
        :param birth_date: employee birth_date
        :param salary: employee salary
        :param department: department employee works in
        """
        self.name = name
        self.birth_date = birth_date
        self.salary = salary
        self.department = department
        self.uuid = str(uuid.uuid4())

    @property
    def age(self):
        """
        Determines age of the employee.
        :return: result value of age
        """
        return date.today().year - self.birth_date.year

    def __repr__(self):
        """
        String representation of EmployeeModel class.
        :return: name and birth_date and salary of the department
        """
        return f'{self.name},{self.birth_date}, {self.salary}'
