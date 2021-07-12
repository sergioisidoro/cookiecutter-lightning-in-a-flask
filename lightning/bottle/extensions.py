"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_migrate import Migrate

migrate = Migrate()