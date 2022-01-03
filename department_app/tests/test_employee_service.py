"""
Module used to test department service, it
defines the following class:
- TestEmployeeService to test the department service functionality
"""
import datetime
from datetime import datetime, date

from department_app.tests.testconf import BaseTestCase
from department_app.models.employee import EmployeeModel
from department_app.service.employee import EmployeeService
from department_app.extensions import db


class TestEmployeeService(BaseTestCase):
    """
    Employee Service test class.
    """
    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        super().setUp()
        self.employee1 = EmployeeModel('Dylan Miller', date(1991, 9, 2), 2400)
        self.employee2 = EmployeeModel('Jennifer Bales', date(1983, 8, 2), 2200)
        db.session.add(self.employee1)
        db.session.add(self.employee2)
        db.session.commit()
        self.employee_service = EmployeeService()

    # def tearDown(self):
    #     super().tearDown()

    def test_find_by_uuid(self):
        """
        Checks whether department is retrieved and returned
        from the database by its uuid.
        """
        uuid = self.employee1.uuid
        self.assertEqual(self.employee1, self.employee_service.find_by_uuid(uuid))

    def test_find_all(self):
        """
        Checks whether all the saved departments are retrieved
        and returned successfully from the database.
        """
        self.assertEqual(2, len(self.employee_service.find_all()))

    def test_no_employee_found(self):
        """
        Checks whether no departments are retrieved and returned
        from the database if none of them were saved.
        """
        db.session.delete(self.employee1)
        db.session.delete(self.employee2)
        db.session.commit()
        self.assertEqual(0, len(self.employee_service.find_all()))

    def test_save_to_db(self):
        """
        Checks whether new department is successfully
        saved to the database.
        """
        employee_new = EmployeeModel('John Parker', date(1988, 10, 1), 3000)
        self.employee_service.save_to_db(employee_new)
        self.assertEqual(3, EmployeeModel.query.count())

    def test_delete_from_db(self):
        """
        Checks whether an existing department is successfully
        deleted from the database and None is returned doing
        search by uuid.
        """
        self.employee_service.delete_from_db(self.employee1)
        self.assertEqual(None, EmployeeModel.query.filter_by(
            uuid=self.employee1.uuid).first())

    def test_update_in_db(self):
        """
        Checks whether an existing department is successfully
        updated in the database.
        """
        self.employee1.name = 'Tony Smith'
        self.employee1.birth_date = date(1993, 9, 2)
        self.employee1.salary = 2200
        self.employee_service.update_in_db()
        updated = EmployeeModel.query.filter_by(uuid=self.employee1.uuid).first()
        self.assertEqual('Tony Smith', updated.name)
        self.assertEqual(datetime(1993, 9, 2, 0, 0), updated.birth_date)
        self.assertEqual(2200, updated.salary)

    def test_find_by_birth_date(self):
        """
        Checks whether all the employees by certain birth date are
        successfully retrieved and returned from the database.
        """
        self.assertEqual([self.employee1],
                         self.employee_service.find_by_birth_date(
                             datetime(1991, 9, 2, 0, 0)))

    def test_find_by_birth_date_empty_list(self):
        """
        Checks whether an empty list is returned in case no employees
        by certain birth date are found in the database.
        """
        self.assertEqual([],
                         self.employee_service.find_by_birth_date
                         (datetime(2000, 6, 1, 0, 0))
                         )

    def test_find_by_birth_period(self):
        """
        Checks whether all the employees born in the period between dates are
        successfully retrieved and returned from the database.
        """
        self.assertEqual([self.employee1],
                         self.employee_service.find_by_birth_period(
                             datetime(1985, 8, 15, 0, 0),
                             datetime(1996, 5, 7, 0, 0))
                         )

    def test_find_by_birth_period_empty_list(self):
        """
        Checks whether an empty list is returned in case no employees
        are found in the database, born in period between dates.
        """
        self.assertEqual([],
                         self.employee_service.find_by_birth_period(
                             datetime(1999, 7, 13, 0, 0),
                             datetime(2020, 8, 4, 0, 0))
                         )
