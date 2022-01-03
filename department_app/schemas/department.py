"""
Department schema module used to serialize and deserialize departments, this module
defines the following classes:
- DepartmentSchema which is department serialization and deserialization schema
"""
from marshmallow import fields

from department_app.extensions import ma
from department_app.schemas.employee import EmployeeSchema
from department_app.models.department import DepartmentModel
from department_app.service.department import DepartmentService

# pylint: disable=too-many-ancestors
class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    """
    Department serialization and deserialization schema
    """
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metadata of department schema
        """
        # model to generate schema from
        model = DepartmentModel
        # deserialize to model schema
        load_instance = True
        # include foreign key into schema
        include_fk = True
        # exclude id from schema
        exclude = ('id',)
        # fields provided only for serialization
        dump_only = ('department_uuid',)
    # employees working in the department nested list
    employees = ma.Nested(EmployeeSchema, many=True)   # pylint: disable=E1101
    # number of employees working in the department
    employees_count = fields.Method('count_employees', dump_only=True)
    # an average salary of employees working in the department
    average_salary = fields.Method('get_average_salary', dump_only=True)
    # an average age of employees working in the department
    employees_average_age = fields.Method('get_employees_average_age', dump_only=True)

    @classmethod
    def count_employees(cls, department):
        """
        Calculates a number of employees working in the department.
        :param department: department object
        :return: amount of the employees
        """
        return DepartmentService.find_employees_count(department)

    @classmethod
    def get_average_salary(cls, department):
        """
        Calculates an average salary of employees working in the department.
        :param department: department object
        :return: average salary of all the employees in the department
        """
        return DepartmentService.find_employees_average_salary(department)

    @classmethod
    def get_employees_average_age(cls, department):
        """
        Calculate an average age of employees working in the department.
        :param department: department object
        :return: average age of all the employees in the department
        """
        return DepartmentService.find_employees_average_age(department)
