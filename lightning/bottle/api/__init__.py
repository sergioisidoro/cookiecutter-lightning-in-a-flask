from bottle.api.resources.users import users_api_blueprint
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

root_api_blueprint = Blueprint(
    'api', 'api', url_prefix='/api/v1',
    description='RootApi'
)


@root_api_blueprint.before_request
@jwt_required(optional=True)
def before_request():
    """
    All routes are optionally required to provide JWT.
    This means curernt user is available (or None) on all
    api routes.
    """
    pass


def register_api_blueprints(api):
    root_api_blueprint.register_blueprint(users_api_blueprint)

    api.register_blueprint(root_api_blueprint)
