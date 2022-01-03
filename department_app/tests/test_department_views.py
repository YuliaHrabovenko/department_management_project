"""
This module is used to test department views, it
defines the following class:
- TestDepartmentViews to test department views functionality.
"""

from http import HTTPStatus

from department_app.tests.testconf import BaseTestCase


class TestDepartmentViews(BaseTestCase):
    """
    Department views test class.
    """
    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        super().setUp()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_departments(self):
        """
        Checks whether get response to /departments
        returns a status code 200
        """
        response = self.client.get('/departments')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_department(self):
        """
        Checks whether get response to /add_department
        returns a status code 200
        """
        response = self.client.get('/add_department')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_department(self):
        """
        Checks whether get response to /edit_department/<uuid>
        returns a status code 200
        """
        response = self.client.get('/edit_department/uuid')
        self.assertEqual(response.status_code, HTTPStatus.OK)
