"""
File with database configuration.
"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
server = os.environ.get('MYSQL_SERVER')
database = os.environ.get('MYSQL_DATABASE')
key = os.environ.get('SECRET_KEY')


# pylint: disable=too-few-public-methods
class Config:
    """
    Config class.
    """
    DEBUG = True
    # SECRET_KEY = secrets.token_hex(32)
    SECRET_KEY = key
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{server}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
