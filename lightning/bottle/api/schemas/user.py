from bottle.models import User
from bottle.db import db
from bottle.extensions import ma


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    admin = ma.Bool(dump_only=True)
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)


class UserQueryArgsSchema(ma.Schema):
    pass
