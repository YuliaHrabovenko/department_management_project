"""
This module is used to test employee views, it
defines the following class:
- TestEmployeeViews to test employee views functionality.
"""
from http import HTTPStatus

from department_app.tests.testconf import BaseTestCase


class TestEmployeeViews(BaseTestCase):
    """
    Employee views test class.
    """
    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        super().setUp()
        self.app.testing = True
        self.client = self.app.test_client()

    # def tearDown(self):
    #     """
    #     Defines instructions that will be executed after each test.
    #     """
    #     super().tearDown()

    def test_employees(self):
        """
        Checks whether get response to /employees
        returns a status code 200.
        """
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_employee(self):
        """
        Checks whether get response to /add_employee
        returns a status code 200.
        """
        response = self.client.get('/add_employee')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_employee(self):
        """
        Checks whether get response to /edit_employee/<uuid>
        returns a status code 200.
        """
        response = self.client.get('/edit_employee/uuid')
        self.assertEqual(response.status_code, HTTPStatus.OK)
