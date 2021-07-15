from bottle.db import db
from bottle.admin.utils import AuthenticatedModelView
from bottle.models.user import User

class UserAdminView(AuthenticatedModelView):
    can_create = False
    column_exclude_list = ['_password', ]


user_admin_view = UserAdminView(User, db.session)