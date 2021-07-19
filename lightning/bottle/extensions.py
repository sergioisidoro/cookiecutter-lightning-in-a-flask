"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_migrate import Migrate
from passlib.context import CryptContext
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, current_user
from flask_smorest import Api
from flask_cors import CORS
from flask_pundit import FlaskPundit
from authlib.integrations.flask_client import OAuth


class JWTFlaskPundit(FlaskPundit):
    """
    A Wrapper around Flask Pundit so it works with Flask JWT extended,
    so we don't need to constatly pass it to the Pundit Authorizations
    """
    def _get_current_user(self):
        return current_user


jwt_pundit = JWTFlaskPundit(policies_path="bottle.policies")
migrate = Migrate()
ma = Marshmallow()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
api = Api()
jwt = JWTManager()
oauth = OAuth()
cors = CORS()
