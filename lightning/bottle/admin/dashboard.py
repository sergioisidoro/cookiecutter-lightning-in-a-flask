from bottle.admin.utils import AuthenticatedAdminIndexView


class DashboardView(AuthenticatedAdminIndexView):
    def is_visible(self):
        return False
