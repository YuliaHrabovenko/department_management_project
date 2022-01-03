"""
This module defines the following classes:
- DepartmentModel, department model used to represent departments
"""
import uuid
from department_app.extensions import db

# pylint: disable=too-few-public-methods

class DepartmentModel(db.Model):
    """
    The DepartmentModel object represents department table in db.
    """

    # name of the department table in db
    __tablename__ = 'department'

    # id of the department in db
    id = db.Column(db.Integer, primary_key=True)
    # department name column in db
    name = db.Column(db.String(20), unique=True, nullable=False)
    # description column in db for department
    description = db.Column(db.String(120), nullable=False)
    # uuid column in db for department
    uuid = db.Column(db.String(36), unique=True)
    # employees working in the department
    employees = db.relationship(
        'EmployeeModel',
        cascade="all,delete,delete-orphan",
        single_parent=True,
        backref='department',
        lazy=True
    )

    def __init__(self, name, description, employees=[]):
        """
        Constructor of DepartmentModel class.
        :param name: department name
        :param description: department description
        :param employees: list of employees working the department
        """
        self.name = name
        self.description = description
        self.uuid = str(uuid.uuid4())
        self.employees = employees

    def __repr__(self):
        """
        String representation of DepartmentModel class.
        :return: name and description of the department
        """
        return f'{self.name}, {self.description}'
