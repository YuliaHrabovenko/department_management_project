"""
This module is used to test employee api, it
defines the following class:
- TestDepartmentApi to test the department api functionality
"""

import json
from http import HTTPStatus
from unittest.mock import patch
from datetime import date
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from department_app.extensions import db
from department_app.tests.testconf import BaseTestCase
from department_app.models.department import DepartmentModel
from department_app.models.employee import EmployeeModel
from department_app.tests.serialization_funcs import emp_to_json


class TestDepartmentApi(BaseTestCase):
    """
    Employee Api test class.
    """

    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        super().setUp()
        self.app.testing = True
        self.client = self.app.test_client()
        # test data
        self.employee_1 = EmployeeModel('Joe Travis', date(1996, 5, 12), 2000)
        self.employee_2 = EmployeeModel('Lisa Simons', date(1990, 8, 10), 3500)
        self.department = DepartmentModel('Finance', 'Some finance department.')

    # def tearDown(self):
    #     """
    #     Defines instructions that will be executed after each test.
    #     """
    #     super().tearDown()

    @patch('department_app.rest.employee.employee_service.find_all', autospec=True)
    def test_get_employees_success(self, mock_get):
        """
        Checks whether employees are successfully retrieved from database.
        Returns a status code 200 when performing get request to /api/employees.
        :param mock_get: mock get object
        """
        employees = [self.employee_1, self.employee_2]
        mock_get.return_value = employees
        response = self.client.get('/api/employees')
        mock_get.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, [emp_to_json(d) for d in mock_get.return_value])

    @patch('department_app.rest.employee.employee_service.save_to_db', autospec=True)
    def test_post_success(self, mock_post):
        """
        Checks whether employee is successfully saved in the database.
        Returns a status code 200 when performing post request to /api/employees.
        :param mock_post: mock object
        """
        employee = {"name": self.employee_1.name, "salary": self.employee_1.salary,
                    "birth_date": self.employee_1.birth_date.strftime('%Y-%m-%d')}
        response = self.client.post('/api/employees', data=json.dumps(employee),
                                    content_type='application/json')
        # mock_post.assert_called_once()
        mock_post.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(employee['name'], response.json['name'])
        self.assertEqual(employee['salary'], response.json['salary'])
        self.assertEqual(employee['birth_date'], response.json['birth_date'])

    @patch('department_app.rest.employee.EmployeeList.post')
    def test_post_empty_name_fail(self, mock_post):
        """
        Checks whether error message is returned with a status code 400 when an empty
        employee name is provided when performing post request to /api/employees.
        :param mock_post: mock post object
        """
        mock_post.side_effect = BadRequest("Please provide some name.")
        data = {'name': '    ', "salary": self.employee_1.salary,
                "birth_date": self.employee_1.birth_date.strftime('%Y-%m-%d')}
        response = self.client.post('/api/employees', data=json.dumps(data),
                                    content_type='application/json')
        mock_post.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, {'message': 'Please provide some name.'})

    @patch('department_app.rest.employee.EmployeeList.post')
    def test_post_employee_validation_error(self, mock_post):
        """
        Checks whether validation error is raised with a status code 400 when request data
        does not meet schema requirements when performing post request to /api/employees.
        :param mock_post: mock post object
        """
        mock_post.side_effect = ValidationError("Validation error message.")
        employee = {'name': self.employee_1.name}
        with self.assertRaises(ValidationError) as exception:
            response = self.client.post('/api/employees', data=json.dumps(employee),
                                        content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        mock_post.assert_called_once()
        self.assertEqual("Validation error message.", exception.exception.messages[0])

    @patch('department_app.rest.employee.employee_service.find_by_uuid', autospec=True)
    def test_get_employee_from_mock_db(self, mock_get):
        """
        Checks whether employee with given uuid is returned with a status code 200
        when performing get request to /api/employee/<uuid>
        :param mock_get: mock get object
        """
        department = DepartmentModel('Finance', 'Some finance department.')
        self.employee_1.department = department
        mock_get.return_value = self.employee_1
        expected_value = emp_to_json(self.employee_1)
        response = self.client.get(f'/api/employee/{self.employee_1.uuid}')
        mock_get.assert_called_once_with(self.employee_1.uuid)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, expected_value)

    @patch('department_app.rest.employee.employee_service.find_by_uuid')
    def test_get_employee_from_mock_db_fail(self, mock_get):
        """
        Checks whether error message is returned with a status code 404
        when performing get request to /api/employee/<uuid> with fake uuid
        :param mock_get: mock get object
        """
        uuid = 'unknown uuid'
        mock_get.side_effect = NotFound('Employee not found error')
        response = self.client.get(f'/api/employee/{uuid}')
        mock_get.assert_called_once()
        self.assertEqual(response.json, {'message': 'Employee not found error'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @patch('department_app.rest.employee.Employee.put', autospec=True)
    def test_put_employee(self, mock_put):
        """
        Checks whether information about employee in database is updated
        with a status code 200 when performing put request to /api/employee/<uuid>.
        :param mock_put: mock put object
        """
        db.session.add(self.employee_1)
        db.session.commit()
        self.employee_1.name = 'John'
        expected_value = emp_to_json(self.employee_1)
        mock_put.return_value = expected_value
        data = {'name': self.employee_1.name, "salary": self.employee_1.salary,
                "birth_date": self.employee_1.birth_date.strftime('%Y-%m-%d')}
        response = self.client.put(f'/api/employee/{self.employee_1.uuid}', data=json.dumps(data),
                                   content_type='application/json')
        mock_put.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, expected_value)

    @patch('department_app.rest.employee.Employee.put')
    def test_put_employee_empty_name_fail(self, mock_put):
        """
        Checks whether error message with a status code 400 is returned when
        performing put request to /api/employee/<uuid> with empty employee name.
        :param mock_put: mock put object
        """
        mock_put.side_effect = BadRequest("Please provide some name.")
        db.session.add(self.employee_1)
        db.session.commit()
        self.employee_1.name = '   '
        data = {'name': self.employee_1.name, "salary": self.employee_1.salary,
                "birth_date": self.employee_1.birth_date.strftime('%Y-%m-%d')}
        response = self.client.put(f'/api/employee/{self.employee_1.uuid}', data=json.dumps(data),
                                   content_type='application/json')
        mock_put.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, {'message': 'Please provide some name.'})

    @patch('department_app.rest.employee.Employee.put')
    def test_put_employee_validation_error(self, mock_put):
        """
        Checks whether validation error is returned with a status code 400 when request data
        does not meet schema requirements when performing put request to /api/employee/<uuid>.
        :param mock_put: mock put object
        """
        mock_put.side_effect = ValidationError("Validation error message.")

        with self.assertRaises(ValidationError) as exception:
            db.session.add(self.employee_1)
            db.session.commit()
            data = {'name': self.employee_1.name}
            response = self.client.put(f'/api/employee/{self.employee_1.uuid}',
                                       data=json.dumps(data),
                                       content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        mock_put.assert_called_once()
        self.assertEqual("Validation error message.", exception.exception.messages[0])

    @patch('department_app.rest.employee.employee_service.delete_from_db')
    def test_delete_employee_success(self, mock_delete):
        """
        Checks whether employee with given uuid is deleted with a status code 204
        when performing delete request to /api/employee /<uuid>
        """
        db.session.add(self.employee_1)
        db.session.commit()
        uuid = self.employee_1.uuid
        mock_delete.return_value = ''
        response = self.client.delete(f'/api/employee/{uuid}')
        mock_delete.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(
            response.get_data(as_text=True).strip('\n"'),
            ''
        )

    @patch('department_app.rest.employee.employee_service.delete_from_db')
    def test_delete_employee_failure(self, mock_delete):
        """
        Checks whether error message is returned with a status code 404 when performing
        delete request to /api/employee/<uuid> with fake uuid.
        """
        mock_delete.side_effect = NotFound("Employee not found error")
        uuid = 'fake_uuid'
        response = self.client.delete(f'/api/employee/{uuid}')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json, {'message': 'Employee not found error'})

    @patch('department_app.rest.employee.EmployeeSearchList.get')
    def test_get_employees_search_by_date(self, mock_get):
        """
        Checks whether list of employees is returned with status code 200
        when performing get request to /api/employees/search?date={date}
        :param mock_get: mock get object
        """
        mock_get.return_value = [emp_to_json(self.employee_1)]
        search_date = '2000-12-01'
        response = self.client.get(f'/api/employees/search?date={search_date}')
        expected_value = mock_get.return_value
        mock_get.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, expected_value)

    @patch('department_app.rest.employee.EmployeeSearchList.get')
    def test_get_employees_search_by_start_and_end_date(self, mock_get):
        """
        Checks whether list of employees is returned with status code 200 when performing
        get request to /api/employees/search?date={start_date}&end_date={end_date}
        :param mock_get: mock get object
        """
        mock_get.return_value = [emp_to_json(self.employee_1), emp_to_json(self.employee_2)]
        start_date = '1990-01-01'
        end_date = '2000-12-10'
        response = self.client.get(
            f'/api/employees/search?start_date={start_date}&end_date={end_date}'
        )
        expected_value = mock_get.return_value
        mock_get.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, expected_value)
