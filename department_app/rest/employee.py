"""
Employees REST API, this module defines the following classes:
- Employee which is employee API class
- EmployeeList which is employee list API class
- EmployeeSearchList which is employee search API class
"""
from datetime import datetime

from flask import request
from flask_restful import Resource, abort, reqparse
from marshmallow import ValidationError

from department_app.schemas.employee import EmployeeSchema
from department_app.service.employee import EmployeeService
from department_app.service.department import DepartmentService
from department_app.extensions import logger

department_service = DepartmentService()
employee_service = EmployeeService()

employee_schema = EmployeeSchema()
employee_list_schema = EmployeeSchema(many=True)


class Employee(Resource):
    """
    Employee API class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('department_uuid')

    @classmethod
    def get(cls, uuid):
        """
        Fetches an employee by uuid via a service and returns it in json format with a status
        code 200 when success or an error message in json with a 404 status code if employee
        with such an uuid has not been found.
        :param uuid: employee uuid
        :return: json representation of the employee and a status code 200 or an error
        message and a status code 404
        """
        employee = employee_service.find_by_uuid(uuid)
        if not employee:
            logger.info(f'Failed to find employee with uuid: "{uuid}"')
            abort(404, description="Employee not found error")
        return employee_schema.dump(employee), 200

    @classmethod
    def put(cls, uuid):
        """
        Updates a employee by its uuid in case such an employee has been found and returns
        it in json format with status code 200. Returns an error message with status code
        400 when request data does not pass validation or an employee input name is empty.
        :param uuid: employee uuid
        :return: json representation of the employee and a status code 200 or an error
        message and a status code 400
        """
        args = cls.parser.parse_args()
        employee = employee_service.find_by_uuid(uuid)
        try:
            employee = employee_schema.load(request.json, instance=employee)
        except ValidationError as error:
            return error.messages, 400
        if employee.name.isspace():
            logger.info(
                'Failed to edit employee: only whitespaces in employee name.')
            abort(400, message="Please provide some name.")
        employee.department = department_service.find_by_uuid(args['department_uuid'])
        employee_service.update_in_db()
        logger.info(
            f'Succeeded to edit employee with name "{employee.name}", '
            f'birth_date: "{employee.birth_date}", '
            f'salary: "{employee.salary}" and '
            f'department: "{employee.department.name}"')
        return employee_schema.dump(employee), 200

    @classmethod
    def delete(cls, uuid):
        """
        Deletes an employee by its uuid in case employee with such an uuid has been found and
        returns 204 status code. Returns an error message with status code 204 when employee
        with such uuid does not exist.
        :param uuid: employee uuid
        :return: no content message and a status code 204 or an error message with a status code 404
        """
        employee = employee_service.find_by_uuid(uuid)
        if not employee:
            logger.info(f'Failed to delete employee with fake uuid: {uuid}')
            abort(404, message="Employee not found error")
        employee_service.delete_from_db(employee)
        logger.info(
            f'Succeeded to delete employee with name: "{employee.name}"')
        return '', 204


class EmployeeList(Resource):
    """
    Employee list API class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('department_uuid')

    @classmethod
    def get(cls):
        """
         Fetches all the employees via a service and returns them in the list of
         json format data items with status code 200 or en empty list in case no employees
         have been found.

        :return: list of employees in json format and status code 200
        """
        employees = employee_service.find_all()
        return employee_list_schema.dump(employees, many=True), 200

    @classmethod
    def post(cls):
        """
        Creates new employee and returns its json representation with a status code 200.
        Returns an error message with a status code 400 in case request data does not pass
        validation or an input employee name is empty.
        :return: json representation of the employee and a status code 201 or an error
        message and a status code 400
        """
        args = cls.parser.parse_args()
        try:
            employee = employee_schema.load(request.json)
        except ValidationError as error:
            return error.messages, 400
        if employee.name.isspace():
            logger.info(
                'Failed to add a new employee: only whitespaces in employee name.')
            abort(400, description="Employee name should not contain only whitespaces.")
        employee.department = department_service.find_by_uuid(args['department_uuid'])
        employee_service.save_to_db(employee)
        name = employee.name
        logger.info(
            f'Succeeded to add employee with name "{name}"')
        return employee_schema.dump(employee), 201


class EmployeeSearchList(Resource):
    """
    Employee search API class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('date')
    parser.add_argument('start_date')
    parser.add_argument('end_date')

    @classmethod
    def get(cls):
        """
         Fetches all the employees born in a specific date via a service and returns them
         in the list of json format data items with status code 200. Or fetches all the
         employees born in a given period via a service and returns them in the list of json
         format data with status code 200.

        :return: list of employees in json format and status code 200
        """
        args = cls.parser.parse_args()
        if args['date']:
            date = datetime.strptime(args['date'], '%Y-%m-%d')
            employees = employee_service.find_by_birth_date(date)
            logger.info(f'Search by exact date: "{date}"')
        elif args['start_date'] and args['end_date']:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d')
            employees = employee_service.find_by_birth_period(start_date, end_date)
            logger.info(f'Search by period between dates: from "{start_date}" to "{end_date}"')
        else:
            logger.info('Invalid date input.')
            abort(400, message="Not valid date input")
        return employee_list_schema.dump(employees, many=True), 200
