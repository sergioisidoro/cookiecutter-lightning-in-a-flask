"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_migrate import Migrate
from passlib.context import CryptContext

migrate = Migrate()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
