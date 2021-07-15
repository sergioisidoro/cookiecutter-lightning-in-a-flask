from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView
from bottle.extensions import pwd_context
from flask import request, Response
from bottle.models.user import User


def verify_password(email, password):
    if not email or not password:
        return False

    user = User.query.filter_by(email=email, admin=True).one_or_none()
    if user is None or not pwd_context.verify(password, user.password):
        return False
    else:
        return True


class AuthenticatedModelView(ModelView):

    # If you override is_acessible, be sure to call super!
    def is_accessible(self):
        auth = request.authorization
        if not auth:
            return False
        if not verify_password(auth.username, auth.password):
            return False
        return True

    # If you override is_acessible, be sure to call super!
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return Response(
            "Please log in.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )


class AuthenticatedAdminIndexView(AdminIndexView):

    # If you override is_acessible, be sure to call super!
    def is_accessible(self):
        auth = request.authorization
        if not auth:
            return False
        if not verify_password(auth.username, auth.password):
            return False
        return True

    # If you override is_acessible, be sure to call super!
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return Response(
            "Please log in.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )