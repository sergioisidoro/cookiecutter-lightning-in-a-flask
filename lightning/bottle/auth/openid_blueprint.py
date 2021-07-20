import string
import random
from flask import Blueprint, jsonify, request
from bottle.extensions import oauth
from bottle.db import db
from bottle.models import User
from bottle.auth.helpers import (
  build_login_success_response,
)

open_id_blueprint = Blueprint("oauth", __name__, url_prefix="/oauth")


def tmp_password_generator():
    all = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.sample(all, 50))


def valiate_token_and_get_user_info(client, bearer_auth):

    if not bearer_auth:
        return None

    auth_token = bearer_auth.replace('Bearer ', '')

    # TODO: properly introspect the token with introspection_endpoint
    # when client introspection is supported by authlib

    structured_token = {
      'access_token': auth_token
    }

    userinfo = client.userinfo(token=structured_token)
    return userinfo


@open_id_blueprint.route('/<provider>/token-exchange/login')
def exchange_login(provider):
    """
    Providing an access_token bearer (eg. aquired by an SPA via PKCE)
    in the Authorization header, make a call to the Openid connect identity
    server requesting infromation for the user, and return an exchanged token
    for logging in to the rest API
    """
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"msg": "Unsupported"}), 400

    userinfo = valiate_token_and_get_user_info(
        client,
        request.headers.get('Authorization')
    )

    if not userinfo or not userinfo['email']:
        return jsonify({"msg": "Isufficient data"}), 400

    user = User.query.filter_by(email=userinfo['email']).one_or_none()

    if user is None:
        return jsonify({"msg": "Bad credentials"}), 400

    result = build_login_success_response(user)

    return jsonify(result), 200


@open_id_blueprint.route('/<provider>/token-exchange/register')
def exchange_register(provider):
    """
    Providing a OpenID connect bearer token (eg. aquired by an SPA via PKCE)
    in the Authorization header, make a call to the Openid connect identity
    server requesting infromation for the user, and return an exchanged token
    for registering and logging in a user to the REST API
    """
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"msg": "Unsupported"}), 400

    userinfo = valiate_token_and_get_user_info(
        client,
        request.headers.get('Authorization')
    )

    if not userinfo or not userinfo['email']:
        return jsonify({"msg": "Isufficient data"}), 400

    user = User.query.filter_by(email=userinfo['email']).one_or_none()

    if user is not None:
        return jsonify({"msg": "User already exists"}), 409

    # Additional properties that can be used (depending on the provider)
    # 'given_name', 'family_name', 'nickname': 'smaisidoro', 'locale'
    # https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse
    new_data = {
      "email": userinfo['email'],
      "password": tmp_password_generator()
    }

    user = User(**new_data)
    db.session.add(user)
    db.session.commit()
    result = build_login_success_response(user)
    return jsonify(result), 200
