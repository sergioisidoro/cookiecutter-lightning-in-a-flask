from bottle.api.resources.users import users_api_blueprint

from flask_smorest import Blueprint

root_api_blueprint = Blueprint(
    'api', 'api', url_prefix='/api/v1',
    description='RootApi'
)

def register_api_blueprints(api):
    root_api_blueprint.register_blueprint(users_api_blueprint)

    api.register_blueprint(root_api_blueprint)
