
from flask_admin import Admin
from bottle.admin.user import user_admin_view
from bottle.admin.dashboard import DashboardView

admin = Admin(
    name='Adminstration',
    index_view=DashboardView()
)

# Please use only authenticated
admin.add_view(user_admin_view)
