"""
File with database configuration.
"""
import os
import secrets

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
server = os.environ.get('MYSQL_SERVER')
database = os.environ.get('MYSQL_DATABASE')


# pylint: disable=too-few-public-methods
class Config:
    """
    Config class.
    """
    DEBUG = True
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{server}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
