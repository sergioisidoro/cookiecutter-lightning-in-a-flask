from bottle.api.resources.users import users_api_blueprint
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint


# FIX ME - Turn into a nested blueprint once this issue is solved
# https://github.com/marshmallow-code/flask-smorest/issues/261


def register_api_blueprints(api):
    api.register_blueprint(users_api_blueprint, url_prefix="/api/v1/users")

