from bottle.models import User
from bottle.db import db
from bottle.extensions import ma
from bottle.api.utils import AutoSchema


class UserSchema(AutoSchema):

    id = ma.Int(dump_only=True)
    admin = ma.Bool(dump_only=True)
    password = ma.String(required=True)

    class Meta:
        model = User
        sqla_session = db.session
        exclude = ("_password",)


class UserQueryArgsSchema(ma.Schema):
    pass
