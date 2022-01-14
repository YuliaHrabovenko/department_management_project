"""
This module is used to test department api, it
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
from department_app.tests.serialization_funcs import dep_to_json
from department_app.models.department import DepartmentModel
from department_app.models.employee import EmployeeModel


class TestDepartmentApi(BaseTestCase):
    """
    Department Api test class.
    """
    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        super().setUp()
        self.app.testing = True
        self.client = self.app.test_client()
        # test data
        self.department1 = DepartmentModel('Finance', 'Some finance department.')
        self.department2 = DepartmentModel('Management', 'Some management department.')

    # def tearDown(self):
    #     """
    #     Defines instructions that will be executed after each test.
    #     """
    #     super().tearDown()

    @patch('department_app.rest.department.department_service.find_all', autospec=True)
    def test_get_departments_success(self, mock_get):
        """
        Checks whether departments are successfully retrieved from database.
        Returns a status code 200 when performing get request to /api/departments.
        :param mock_get: mock get object
        """
        departments = [self.department1, self.department2]
        mock_get.return_value = departments
        response = self.client.get('/api/departments')
        mock_get.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, [dep_to_json(d) for d in mock_get.return_value])

    @patch('department_app.rest.department.department_service.save_to_db', autospec=True)
    def test_post_success(self, mock_post):
        """
        Checks whether department is successfully saved in the database.
        Returns a status code 200 when performing post request to /api/departments.
        :param mock_post: mock object
        """
        department = {'name': 'Finance', 'description': 'Some finance department.'}
        response = self.client.post('/api/departments', data=json.dumps(department),
                                    content_type='application/json')
        mock_post.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn(department['name'], response.json['name'])
        self.assertIn(department['description'], response.json['description'])

    @patch('department_app.rest.department.DepartmentList.post')
    def test_post_empty_name_failure(self, mock_post):
        """
        Checks whether error message is returned with a status code 400 when an empty
        department name is provided when performing post request to /api/departments.
        :param mock_post: mock post object
        """
        mock_post.side_effect = BadRequest(
            "Empty department name is not allowed. Please provide some.")
        data = {'name': '    ', 'description': 'New marketing department.'}
        response = self.client.post('/api/departments', data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json,
                         {'message': 'Empty department name is not allowed. Please provide some.'}
                         )

    @patch('department_app.rest.department.DepartmentList.post')
    def test_post_existing_name_failure(self, mock_post):
        """
        Checks whether error message is returned with a status code 400 when an existing
        department name is provided while performing post request to /api/departments.
        :param mock_post: mock post object
        """
        department = self.department1
        db.session.add(department)
        db.session.commit()
        mock_post.side_effect = BadRequest(
            f"Department with name {department.name} already exists.")
        data = {'name': 'Finance', 'description': 'New marketing department.'}
        response = self.client.post('/api/departments',
                                    data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json,
                         {'message': f"Department with name {department.name} already exists."})

    @patch('department_app.rest.department.DepartmentList.post')
    def test_post_department_validation_error(self, mock_post):
        """
        Checks whether validation error is raised with a status code 400 when request data
        does not meet schema requirements when performing post request to /api/departments.
        :param mock_post: mock post object
        """
        mock_post.side_effect = ValidationError("Validation error message.")
        department = {'name': 'Finance'}
        with self.assertRaises(ValidationError) as exception:
            response = self.client.post('/api/departments', data=json.dumps(department),
                                        content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual("Validation error message.", exception.exception.messages[0])

    @patch('department_app.rest.department.department_service.find_by_uuid', autospec=True)
    def test_get_department_success(self, mock_get):
        """
        Checks whether department with given uuid is returned with a status code 200
        when performing get request to /api/department/<uuid>
        :param mock_get: mock get object
        """
        department = DepartmentModel('Finance', 'Some finance department.')
        department.employees = [EmployeeModel('John Williams', date(1996, 5, 12), 2000)]
        mock_get.return_value = department
        expected_value = dep_to_json(department)
        response = self.client.get(f'/api/departments/{department.uuid}')
        mock_get.assert_called_once_with(department.uuid)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, expected_value)

    @patch('department_app.rest.department.department_service.find_by_uuid')
    def test_get_department_failure(self, mock_get):
        """
        Checks whether error message is returned with a status code 404
        when performing get request to /api/department/<uuid> with fake uuid
        :param mock_get: mock get object
        """
        uuid = 'unknown uuid'
        mock_get.side_effect = NotFound('Department not found error')
        response = self.client.get(f'/api/departments/{uuid}')
        self.assertEqual(response.json, {'message': 'Department not found error'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @patch('department_app.rest.department.Department.put', autospec=True)
    def test_put_department(self, mock_put):
        """
        Checks whether information about department in database is updated
        with a status code 200 when performing put request to /api/department/<uuid>.
        :param mock_put: mock put object
        """
        # db.session.add(self.department1)
        # db.session.commit()
        self.department1.name = 'Marketing'
        expected_value = dep_to_json(self.department1)
        mock_put.return_value = expected_value
        data = {'name': self.department1.name,
                'description': self.department1.description
                }
        response = self.client.put(f'/api/departments/{self.department1.uuid}',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, expected_value)

    @patch('department_app.rest.department.Department.put')
    def test_put_department_empty_name(self, mock_put):
        """
        Checks whether error message with a status code 400 is returned when
        performing put request to /api/department/<uuid> with empty department name.
        :param mock_put: mock put object
        """
        mock_put.side_effect = BadRequest(
            "Empty department name is not allowed. Please provide some.")
        # db.session.add(self.department1)
        # db.session.commit()
        self.department1.name = '   '
        data = {'name': self.department1.name, 'description': self.department1.description}
        response = self.client.put(f'/api/departments/{self.department1.uuid}',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json,
                         {'message': 'Empty department name is not allowed. Please provide some.'})

    @patch('department_app.rest.department.Department.put')
    def test_put_department_validation_error(self, mock_put):
        """
        Checks whether validation error is returned with a status code 400 when request data
        does not meet schema requirements when performing put request to /api/department/<uuid>.
        :param mock_put: mock put object
        """
        mock_put.side_effect = ValidationError("Validation error message.")

        with self.assertRaises(ValidationError) as exception:
            # db.session.add(self.department1)
            # db.session.commit()
            data = {'description': self.department1.description}
            response = self.client.put(f'/api/departments/{self.department1.uuid}',
                                       data=json.dumps(data),
                                       content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual("Validation error message.", exception.exception.messages[0])

    @patch('department_app.rest.department.department_service.delete_from_db')
    def test_delete_department_success(self, mock_delete):
        """
        Checks whether department with given uuid is deleted with a status code 204
        when performing delete request to /api/department/<uuid>
        """
        # pylint: disable=no-member
        db.session.add(self.department1)
        db.session.commit()
        uuid = self.department1.uuid
        mock_delete.return_value = ''
        response = self.client.delete(f'/api/departments/{uuid}')
        mock_delete.assert_called_once()
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(
            response.get_data(as_text=True).strip('\n"'),
            ''
        )

    @patch('department_app.rest.department.department_service.delete_from_db')
    def test_delete_department_failure(self, mock_delete):
        """
        Checks whether error message is returned with a status code 404 when performing
        delete request to /api/department/<uuid> with fake uuid.
        """
        mock_delete.side_effect = NotFound("Department not found error")
        uuid = 'fake_uuid'
        response = self.client.delete(f'/api/departments/{uuid}')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json, {'message': 'Department not found error'})
