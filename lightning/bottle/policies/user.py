from bottle.policies.utils import SQLAlchemyPolicy


class UserPolicy(SQLAlchemyPolicy):
    def __init__(self, user, resource):
        self.user = user
        self.resource = resource

    def get(self):
        return self.is_admin_or_self()

    def create(self):
        return self.is_admin_or_self()

    def update(self):
        return self.is_admin_or_self()

    def list(self):
        return self.user.admin

    def delete(self):
        return self.is_admin_or_self()

    def scope(self):
        if self.user.admin:
            return self.resource.query
        return self.resource.query.filter_by(id)

    # HELPERS
    def is_admin_or_self(self):
        return self.user.admin or self.user.id == self.resource.id
