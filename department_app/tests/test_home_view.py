"""
This module is used to test home page view, it
defines the following class:
- TestHomeView to test home page view functionality.
"""
from http import HTTPStatus
from department_app.tests.testconf import BaseTestCase


class TestHomeView(BaseTestCase):
    """
    Home view test class.
    """
    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        super().setUp()
        self.app.testing = True
        self.client = self.app.test_client()

    # def tearDown(self):
    #     super().tearDown()

    def test_home(self):
        """
        Checks whether get response to /
        returns a status code 200.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
