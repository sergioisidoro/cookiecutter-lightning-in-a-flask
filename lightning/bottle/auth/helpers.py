"""Various helpers for auth.
"""
import datetime
from flask import current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token, get_jti
)
from sqlalchemy.orm.exc import NoResultFound

from bottle.db import db
from bottle.models.user import UserSession


def refresh_session(user, refresh_jti):
    session = UserSession.query.filter_by(refresh_token_id=refresh_jti).one()
    if session.revoked:
        return None
    else:
        session.refreshe += 1
        db.session.commit()
        new_token = create_access_token(identity=user)
        return new_token


def create_session_and_session_token(user):
    token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    session = UserSession(
        user=user,
        token_id=get_jti(token),
        refresh_token_id=get_jti(refresh_token),
        valid_until=(
            datetime.datetime.utcnow() +
            app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        ),
        refreshable_unil=(
            datetime.datetime.utcnow() +
            app.config["JWT_REFRESH_TOKEN_EXPIRES"]
        )
    )
    db.session.add(session)
    db.session.commit()
    return (token, refresh_token)


def is_token_revoked(jwt_headers, jwt_payload):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = jwt_payload["jti"]
    try:
        if jwt_payload['type'] == "refresh":
            session = UserSession.query.filter_by(refresh_token_id=jti).one()
        else:
            session = UserSession.query.filter_by(token_id=jti).one()
        return session.revoked
    except NoResultFound:
        return True


def revoke_token(token_jti, user):
    """Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    """
    try:
        token = UserSession.query.filter_by(token_id=token_jti).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception("Could not find the token {}".format(token_jti))


def revoke_refresh_token(token_jti, user):
    """Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    """
    try:
        token = UserSession.query.filter_by(refresh_token_id=token_jti).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception("Could not find the token {}".format(token_jti))
