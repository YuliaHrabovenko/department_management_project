"""
Departments REST API, this module defines the following classes:
- Department which is department API class
- DepartmentList which is department list API class
"""
from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError

from department_app.schemas.department import DepartmentSchema
from department_app.service.department import DepartmentService
from department_app.extensions import logger

department_service = DepartmentService()
department_schema = DepartmentSchema()
department_list_schema = DepartmentSchema(many=True)


class Department(Resource):
    """
    Department API class
    """
    @classmethod
    def get(cls, uuid):
        """
        Fetches a department by uuid via a service and returns it in json format with a status
        code 200 when success or an error message in json with a 404 status code if department
        with such an uuid has not been found.
        :param uuid: department uuid
        :return: json representation of the department and a status code 200 or an error
        message and a status code 404
        """
        department = department_service.find_by_uuid(uuid)
        if not department:
            logger.info(f'Failed to find department with uuid: "{uuid}"')
            abort(404, description="Department not found error")
        return department_schema.dump(department), 200

    @classmethod
    def put(self, uuid):
        """
        Updates a department by its uuid in case such a department has been found and returns
        it in json format with status code 200. Returns an error message with status code
        400 when request data does not pass validation or a department input name is empty.
        :param uuid: department uuid
        :return: json representation of the department and a status code 200 or an error
        message and a status code 400
        """
        department = department_service.find_by_uuid(uuid)
        try:
            department = department_schema.load(request.json, instance=department)
        except ValidationError as error:
            return error.messages, 400
        if department.name.isspace():
            logger.info(
                f'Failed to edit department: only whitespaces in department name.')
            abort(400, message="Empty department name is not allowed. Please provide some.")
        department_service.update_in_db()
        logger.info(
            f'Succeeded to update department: name "{department.name}", description "{department.description}"')
        return department_schema.dump(department), 200

    @classmethod
    def delete(cls, uuid):
        """
        Deletes a department by its uuid in case department with such an uuid was found and
        returns 204 status code. Returns an error message with status code 204 when department
        with such uuid does not exist.
        :param uuid: department uuid
        :return: no content message and a status code 204 or an error message with a status code 404
        """
        department = department_service.find_by_uuid(uuid)
        if not department:
            logger.info(f'Failed to delete department with fake uuid: {uuid}')
            abort(404, message="Department not found error")
        logger.info(
            f'Succeeded to delete department with name: "{department.name}"')
        department_service.delete_from_db(department)
        return '', 204


class DepartmentList(Resource):
    """
    Department list API class
    """
    @classmethod
    def get(cls):
        """
         Fetches a list of all departments via a service and returns them in the list of
         json format data items with status code 200 or en empty list in case no departments
         have been found.

        :return: list of departments in json format and status code 200
        """
        departments = department_service.find_all()
        return department_list_schema.dump(departments), 200

    @classmethod
    def post(cls):
        """
        Creates new department and returns its json representation with a status code 200.
        Returns an error message with a status code 400 in case request data does not pass
        validation or an input department name is empty.
        :return: json representation of the department and a status code 201 or an error
        message and a status code 400
        """
        name = request.json['name']
        department_exists_check = department_service.find_by_name(name)
        if department_exists_check:
            logger.info(f'Failed to add a new department: department with name {name} already exists')
            abort(400, description=f"Department with name {name} already exists.")
        try:
            department = department_schema.load(request.json)
        except ValidationError as error:
            return error.messages, 400
        if department.name.isspace():
            logger.info(
                f'Failed to add a new department: only whitespaces in department name.')
            abort(400, description="Department name should not contain only whitespaces.")
        department_service.save_to_db(department)
        logger.info(
            f'Succeeded to add department: name "{department.name}", description "{department.description}"')
        return department_schema.dump(department), 201
