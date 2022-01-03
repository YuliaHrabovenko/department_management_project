"""
Base class for testing with functions running before and after each test defined.
"""
import unittest

from department_app.extensions import db
from department_app import create_app


class BaseTestCase(unittest.TestCase):
    """
    Base test class.
    """
    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        self.app = create_app()
        # Turn on testing mode
        self.app.config['TESTING'] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tests/test_dbase.db"
        # Dynamically bind SQLAlchemy to application
        db.init_app(self.app)
        self.app.app_context().push()
        db.create_all()
        # self.app.testing = True
        # self.client = self.app.test_client()

    def tearDown(self):
        """
        Defines instructions that will be executed after each test.
        """
        db.session.remove()
        db.drop_all()
