from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from bottle.extensions import jwt_pundit
from bottle.db import db

from bottle.models.user import User
from bottle.api.schemas.user import UserSchema, UserQueryArgsSchema

users_api_blueprint = Blueprint(
    'users', 'users', url_prefix='/users',
    description='Operations on users'
)


@users_api_blueprint.route('/')
class Users(MethodView):

    decorators = [jwt_required()]

    @users_api_blueprint.arguments(UserQueryArgsSchema)
    @users_api_blueprint.response(200, UserSchema(many=True))
    def get(self, args):
        """List users"""
        if not jwt_pundit.authorize(User, action='list'):
            return 403
        user_query = jwt_pundit.policy_scope(User)
        users = user_query.filter_by(**args)
        return users

    @users_api_blueprint.arguments(UserSchema)
    @users_api_blueprint.response(201, UserSchema)
    def post(self, new_data):
        """Add a new user"""
        user = User(**new_data)
        if not jwt_pundit.authorize(user, action='create'):
            return 403
        db.session.add(user)
        db.session.commit()
        return user


@users_api_blueprint.route('/<user_id>')
class UserById(MethodView):

    decorators = [jwt_required()]

    @users_api_blueprint.response(200, UserSchema)
    def get(self, user_id):
        """Get user by ID"""
        user = User.query.get_or_404(user_id)
        if not jwt_pundit.authorize(user, action='get'):
            return "Unauthorized", 401
        return user

    @users_api_blueprint.arguments(UserSchema)
    @users_api_blueprint.response(200, UserSchema)
    def put(self, update_data, user_id):
        """Update existing user"""
        user = User.query.get_or_404(user_id)
        if not jwt_pundit.authorize(user, action='update'):
            return "Unauthorized", 401
        # users_api_blueprint.check_etag(user, UserSchema)
        UserSchema().update(user, update_data)
        db.session.add(user)
        db.session.commit()
        return user

    @users_api_blueprint.response(204)
    def delete(self, user_id):
        """Delete user"""
        user = User.query.get_or_404(user_id)
        if not jwt_pundit.authorize(user, action='delete'):
            return "Unauthorized", 401
        # users_api_blueprint.check_etag(user, UserSchema)
        db.session.delete(user)
        db.session.commit()
