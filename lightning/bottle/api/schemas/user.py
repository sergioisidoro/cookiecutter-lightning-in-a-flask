from bottle.models import User
from bottle.db import db
from bottle.extensions import ma
from bottle.api.utils import AutoSchema


class UserSchema(AutoSchema):

    id = ma.auto_field(dump_only=True)
    password = ma.String(load_only=True)

    class Meta:
        model = User
        sqla_session = db.session
        exclude = ("_password", "admin")


class UserCreateSchema(UserSchema):
    # Special case for password, since it's a special @hybrid property,
    # and because we don't want to make it mandatory on every update.
    password = ma.String(load_only=True, required=True)


class UserQueryArgsSchema(ma.Schema):
    pass
