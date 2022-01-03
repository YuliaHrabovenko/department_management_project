"""
Employee schema module used to serialize and deserialize departments, this module
defines the following classes:
- EmployeeSchema which is employee serialization and deserialization schema
"""
from marshmallow import fields

from department_app.extensions import ma
from department_app.models.employee import EmployeeModel


# pylint: disable=too-many-ancestors
class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    """
   Employee serialization and deserialization schema
   """
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metadata of employee schema
        """
        # model to generate schema from
        model = EmployeeModel
        # include foreign key into schema
        include_fk = True
        # deserialize to model schema
        load_instance = True
        # exclude id and department_id from schema
        exclude = ('id', 'department_id')

    # employee`s date of birth
    birth_date = fields.DateTime(format='%Y-%m-%d')
    # employee`s age provided only for serialization
    age = fields.Method('get_age', dump_only=True)
    # name of the department an employee works in
    department = fields.Method('get_department_name')
    # uuid of the department an employee works in
    department_uuid = fields.Method('get_department_uuid')

    @classmethod
    def get_age(cls, employee):
        """
        Returns  age of an employee
        :param employee: an employee object
        :return: value of employee`s age
        """
        return employee.age

    @classmethod
    def get_department_name(cls, employee):
        """
        Returns name of the department an employee works in or
        'not added' information in case it has no department yet.
        :param employee: employee`s object
        :return: name of the department
        """
        try:
            return f"{employee.department.name}"
        except AttributeError:
            return 'Not added'

    @classmethod
    def get_department_uuid(cls, employee):
        """
        Returns uuid of the department an employee works in or
        'not added' information in case it has no department yet.
        :param employee: employee`s object
        :return: name of the department
        """
        try:
            return f"{employee.department.uuid}"
        except AttributeError:
            return 'Not added'
