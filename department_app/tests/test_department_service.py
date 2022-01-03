"""
This module is used to test department api, it
defines the following class:
- TestDepartmentService to test the department work with database
"""
from datetime import date

from department_app.tests.testconf import BaseTestCase
from department_app.models.department import DepartmentModel
from department_app.models.employee import EmployeeModel
from department_app.service.department import DepartmentService
from department_app.extensions import db


class TestDepartmentService(BaseTestCase):
    """
    Department Service test class.
    """
    def setUp(self) -> None:
        """
        Defines instructions that will be executed before each test.
        """
        super().setUp()
        self.department1 = DepartmentModel('Finance', 'Some finance department.')
        self.department2 = DepartmentModel('Management', 'Some management department.')
        self.employee1 = EmployeeModel('Dylan Miller', date(1991, 9, 2), 2400)
        self.employee2 = EmployeeModel('Teressa Atkinson', date(1995, 2, 7), 1700)
        self.employee3 = EmployeeModel('John Arthur', date(1986, 4, 6), 2000)
        self.employee4 = EmployeeModel('Jennifer Bales', date(1983, 8, 2), 2200)

        self.department1.employees = [self.employee1, self.employee2]
        self.department2.employees = [self.employee3, self.employee4]
        db.session.add(self.department1)
        db.session.add(self.department2)
        db.session.commit()
        self.department_service = DepartmentService()

    # def tearDown(self):
    #     """
    #     Defines instructions that will be executed after each test.
    #     """
    #     super().tearDown()

    def test_find_all(self):
        """
        Checks whether all the saved departments are retrieved
        and returned successfully from the database.
        """
        self.assertEqual(2, len(self.department_service.find_all()))

    def test_no_department_found(self):
        """
        Checks whether no departments are retrieved and returned
        from the database if none of them were saved.
        """
        db.session.delete(self.department1)
        db.session.delete(self.department2)
        db.session.commit()
        self.assertEqual(0, len(self.department_service.find_all()))

    def test_find_by_uuid(self):
        """
        Checks whether department is retrieved and returned
        from the database by its uuid.
        """
        uuid = self.department1.uuid
        self.assertEqual(self.department1, self.department_service.find_by_uuid(uuid))

    def test_find_by_name(self):
        """
        Checks whether department is retrieved and returned
        from database by its name.
        """
        self.assertEqual(self.department1,
                         self.department_service.find_by_name(
                             self.department1.name)
                         )

    def test_find_by_name_none(self):
        """
        Checks whether no department is returned from the
        database by fake department name.
        """
        self.assertEqual(None, self.department_service.find_by_name('fake name'))

    def test_save_to_db(self):
        """
        Checks whether new department is successfully
        saved to the database.
        """
        department_new = DepartmentModel('Marketing', 'Marketing department added.')
        self.department_service.save_to_db(department_new)
        self.assertEqual(3, DepartmentModel.query.count())

    def test_update_in_db(self):
        """
        Checks whether an existing department is successfully
        updated in the database.
        """
        self.department1.name = 'R&D'
        self.department1.description = 'Finance changed to R&D department'
        self.department_service.update_in_db()
        updated = DepartmentModel.query.filter_by(uuid=self.department1.uuid).first()
        self.assertEqual('R&D', updated.name)
        self.assertEqual('Finance changed to R&D department', updated.description)

    def test_delete_from_db(self):
        """
        Checks whether an existing department is successfully
        deleted from the database and None is returned doing
        search by uuid.
        """
        self.department_service.delete_from_db(self.department1)
        self.assertEqual(None, DepartmentModel.query.filter_by(uuid=self.department1.uuid).first())

    def test_find_employees_count(self):
        """
        Checks whether an amount of departments is successfully
        returned from the database.
        """
        department = DepartmentModel.query.filter_by(uuid=self.department1.uuid).first()
        self.assertEqual(2, self.department_service.find_employees_count(department))

    def test_find_employees_average_salary(self):
        """
        Checks whether an average salary of employees in the department
        is successfully returned from the database.
        """
        department = DepartmentModel.query.filter_by(uuid=self.department1.uuid).first()
        self.assertEqual(2050, self.department_service.find_employees_average_salary(department))

    def test_find_employees_average_salary_null(self):
        """
        Checks whether an average salary of employees in the department
        equals to null when no employees are added to the department.
        """
        self.department1.employees = []
        db.session.commit()
        department = DepartmentModel.query.filter_by(uuid=self.department1.uuid).first()
        self.assertEqual(0, self.department_service.find_employees_average_salary(department))

    def test_find_employees_average_age(self):
        """
        Checks whether an average age of employees in the department
        is successfully returned from the database.
        """
        department = DepartmentModel.query.filter_by(uuid=self.department1.uuid).first()
        self.assertEqual(29, self.department_service.find_employees_average_age(department))

    def test_find_employees_average_age_null(self):
        """
        Checks whether an average age of employees in the department
        equals to null when no employees are added to the department.
        """
        self.department1.employees = []
        db.session.commit()
        department = DepartmentModel.query.filter_by(uuid=self.department1.uuid).first()
        self.assertEqual(0, self.department_service.find_employees_average_age(department))
