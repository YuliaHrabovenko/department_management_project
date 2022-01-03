"""
Department service module used to realize interaction with database, this module
defines the following class:
- DepartmentService which is a department serialization and deserialization schema
"""
from typing import List

from department_app.extensions import db, logger
from department_app.models.department import DepartmentModel


class DepartmentService:
    """
    Department service used to make database queries.
    """
    @classmethod
    def find_by_uuid(cls, uuid):
        """
        Fetches the department by given uuid from database.
        :param uuid: department`s uuid
        :return: department with given uuid
        """
        try:
            return db.session.query(DepartmentModel).filter_by(uuid=uuid).first()
        except:
            logger.warning('Department search by uuid in the db failed.')

    @classmethod
    def find_by_name(cls, name):
        """
        Fetches the department by given name from database.
        :param uuid: department`s name
        :return: department with given name
        """
        try:
            return db.session.query(DepartmentModel).filter_by(name=name).first()
        except:
            logger.warning('Department search by name in the db failed.')

    @classmethod
    def find_all(cls) -> List[DepartmentModel]:
        """
        Fetches all the departments from database.
        :return: list of all the departments
        """
        try:
            return db.session.query(DepartmentModel).all()
        except:
            logger.warning('List of departments search in the db failed.')


    @classmethod
    def save_to_db(cls, department_object):
        """
        Saves provided department in database.
        :param department_object: given department
        """
        try:
            db.session.add(department_object)
            db.session.commit()
        except:
            logger.warning('Saving department in the db failed.')

    @classmethod
    def update_in_db(cls):
        """
        Updates given department in the database and
        saves changes.
        """
        try:
            db.session.commit()
        except:
            logger.warning('Updating department in the db failed.')

    @classmethod
    def delete_from_db(cls, department_object):
        """
        Deletes provided department from database.
        :param department_object: given department
        """
        try:
            db.session.delete(department_object)
            db.session.commit()
        except:
            logger.warning('Deleting department from the db failed.')

    @classmethod
    def find_employees_count(cls, department_object):
        """
        Calculates the number of employees in the department.
        :param department_object: given department
        :return: amount of the employees
        """
        try:
            return len(department_object.employees)
        except:
            logger.warning('Counting department employees in the db failed.')

    @classmethod
    def find_employees_average_salary(cls, department_object):
        """
        Calculates average salary of employees working in
        the given department.
        :param department_object: given department
        :return: an average salary value
        """
        employees_count = len(department_object.employees)
        try:
            return round(sum(map
                             (lambda employee: employee.salary, department_object.employees)
                             ) / employees_count, 1)
        except ZeroDivisionError:
            return 0

    @classmethod
    def find_employees_average_age(cls, department_object):
        """
        Calculates average age of employees working in
        the given department.
        :param department_object: provided department
        :return: employee`s average age value
        """
        employees_count = len(department_object.employees)
        try:
            return int(round(sum(map
                                 (lambda employee: employee.age, department_object.employees)
                                 ) / employees_count))
        except ZeroDivisionError:
            return 0
