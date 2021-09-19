"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS
# adds significant overhead and will be disabled by default in the future.
# Set it to True or False to suppress this warning.
SQLALCHEMY_TRACK_MODIFICATIONS = False


# API
API_TITLE = 'lightning API'
API_VERSION = 'v1'
OPENAPI_VERSION = '3.0.2'

OPENAPI_URL_PREFIX = 'apidocs'
OPENAPI_SWAGGER_UI_PATH = 'swagger'
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
