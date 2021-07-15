import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from bottle.db import db
from bottle.extensions import pwd_context


class UserSession(db.Model):
    """A user session login attempt and token holder"""
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(36), nullable=False, unique=True)
    refresh_token_id = db.Column(db.String(36), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='sessions', lazy=True)
    revoked = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    valid_until = db.Column(db.DateTime)
    refreshable_unil = db.Column(db.DateTime)
    refreshes = db.Column(db.Integer, default=0)

    # TODO: Include server_side valid_until and refreshable_unil
    # validation
    def is_invalid(self):
        return self.revoked

    def refreshable(self):
        return not self.revoked


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)

    # Admin should be NOT be considered for application logic
    # here admin means a person with full and unconditional access
    # to administration features. Ideally there should be only one of
    # these users.
    admin = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s (%s)>" % (self.id, self.email)
