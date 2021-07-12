from flask.views import MethodView
from flask_smorest import Blueprint, abort

from bottle.db import db

from bottle.models.user import User
from bottle.api.schemas.user import UserSchema, UserQueryArgsSchema

users_api_blueprint = Blueprint(
    'users', 'users', url_prefix='/users',
    description='Operations on users'
)


@users_api_blueprint.route('/')
class Users(MethodView):

    @users_api_blueprint.arguments(UserQueryArgsSchema, location='query')
    @users_api_blueprint.response(200, UserSchema(many=True))
    def get(self, args):
        """List users"""
        return User.query.filter_by(**args)

    @users_api_blueprint.arguments(UserSchema)
    @users_api_blueprint.response(201, UserSchema)
    def post(self, new_data):
        """Add a new user"""
        user = User(**new_data)
        db.session.add(user)
        db.session.commit()
        return user


@users_api_blueprint.route('/<user_id>')
class PetsById(MethodView):

    @users_api_blueprint.response(200, UserSchema)
    def get(self, user_id):
        """Get user by ID"""
        return User.query.get_or_404(user_id)

    @users_api_blueprint.arguments(UserSchema)
    @users_api_blueprint.response(200, UserSchema)
    def put(self, update_data, user_id):
        """Update existing user"""
        user = User.query.get_or_404(user_id)
        users_api_blueprint.check_etag(user, UserSchema)
        UserSchema().update(user, update_data)
        db.session.add(user)
        db.session.commit()
        return user

    @users_api_blueprint.response(204)
    def delete(self, user_id):
        """Delete user"""
        user = User.query.get_or_404(user_id)
        users_api_blueprint.check_etag(user, UserSchema)
        db.session.delete(user)
        db.session.commit()
