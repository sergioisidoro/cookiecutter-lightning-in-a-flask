from bottle.policies.utils import SQLAlchemyPolicy


class UserPolicy(SQLAlchemyPolicy):
    def __init__(self, user, resource):
        self.user = user
        self.resource = resource

    def get(self):
        return self.is_admin_or_self()

    def create(self):
        # Users should be able register
        return True

    def update(self):
        return self.is_admin_or_self()

    def delete(self):
        # For integrity issues, logged in users should not be able to delete
        # themselves.
        return self.user.admin and self.user.id != self.resource.id

    def scope(self):
        if self.user.admin:
            return self.resource.query
        # Add here what other usesrs a user is allowed to see.
        # By default users are only allowed to list themselves
        return self.resource.query.filter_by(id=self.user.id)

    # HELPERS
    def is_admin_or_self(self):
        return self.user.admin or self.user.id == self.resource.id
