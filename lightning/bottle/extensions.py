"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_migrate import Migrate
from passlib.context import CryptContext
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_smorest import Api


migrate = Migrate()
ma = Marshmallow()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
api = Api()
jwt = JWTManager()
