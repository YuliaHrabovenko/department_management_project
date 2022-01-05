"""
Extensions module to avoid circular imports.
"""
import logging
import logging.handlers
import sys

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
api = Api()
ma = Marshmallow()


def get_logger():
    """
    Used to log app and display debug information at the
    debugging level in the console and in a separate file.
    :return: logger object
    """
    # werkzeug_logger = logging.getLogger('werkzeug')
    # werkzeug_logger.setLevel(logging.ERROR)
    # Create logger
    application_logger = logging.getLogger()
    application_logger.setLevel(logging.DEBUG)
    application_logger.handlers.clear()
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        'logfile.log',
        maxBytes=1024 * 1024)
    file_handler.setLevel(logging.DEBUG)
    # Console handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    # Create formatter to show timestamp, logger name and log message in logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Add formatter to file and console handler
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # Add file and console handler to logger
    application_logger.addHandler(file_handler)
    application_logger.addHandler(stream_handler)
    return application_logger


logger = get_logger()
