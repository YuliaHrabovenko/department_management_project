"""
Sources root package.
"""
import os

from flask import Flask
from sqlalchemy_utils import database_exists

from config import Config
from department_app.extensions import db
from department_app.extensions import migrate
from department_app.extensions import logger
from department_app.views import views_bp
from department_app.models.department import DepartmentModel
from department_app.models.employee import EmployeeModel
from department_app.extensions import api
from department_app.rest.department import Department, DepartmentList
from department_app.rest.employee import Employee, EmployeeList, EmployeeSearchList


MIGRATION_DIRECTORY = os.path.join('department_app', 'migrations')


def create_app():
    """
    Create flask application
    :return: the app instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    create_database_if_not_exists(app, db, app.config['SQLALCHEMY_DATABASE_URI'])
    migrate.init_app(app, db, directory=MIGRATION_DIRECTORY)
    register_api_and_blueprint(app)
    api.init_app(app)
    return app


def register_api_and_blueprint(app):
    """
    Attach api routes to the flask app
    """
    app.register_blueprint(views_bp)
    api.app = app
    api.add_resource(DepartmentList, '/api/departments')
    api.add_resource(Department, '/api/department/<uuid>')

    api.add_resource(EmployeeList, '/api/employees')
    api.add_resource(EmployeeSearchList, '/api/employees/search')
    api.add_resource(Employee, '/api/employee/<uuid>')


def create_database_if_not_exists(app, db, database_url):
    """
    Create database if it does not exist
    :param app: app instance
    :param db: db instance
    :param database_url: database url
    """
    if not database_exists(database_url):
        with app.app_context():
            db.create_all()
