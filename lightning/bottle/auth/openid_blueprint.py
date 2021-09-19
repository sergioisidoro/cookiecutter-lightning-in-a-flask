import string
import random
from flask import Blueprint, jsonify, request
from bottle.extensions import oauth
from bottle.db import db
from bottle.models import User
from bottle.auth.helpers import (
  build_login_success_response,
)
from authlib.jose import jwt, JsonWebToken, JsonWebKey

open_id_blueprint = Blueprint("oauth", __name__, url_prefix="/oauth")


def validate_token(client, token, leeway=120):
    """
    Validates the token claims (issuer and client id) before
    sending a requests to the userinfo endpoint, ensuring that
    the toke was issued with the correct audience or client
    (ie, if it's a Google oauth token, that it's not a token
    from another google oauth app).
    """
    def load_key(header, _):
        jwk_set = JsonWebKey.import_key_set(client.fetch_jwk_set())
        try:
            return jwk_set.find_by_kid(header.get('kid'))
        except ValueError:
            # re-try with new jwk set
            jwk_set = JsonWebKey.import_key_set(
                client.fetch_jwk_set(force=True)
            )
            return jwk_set.find_by_kid(header.get('kid'))

    metadata = client.load_server_metadata()
    if 'issuer' in metadata:
        claims_options = {'iss': {'values': [metadata['issuer']]}}

    claims_params = dict(
        client_id=client.client_id,
    )

    alg_values = metadata.get('id_token_signing_alg_values_supported')
    if alg_values:
        _jwt = JsonWebToken(alg_values)
    else:
        _jwt = jwt

    claims = _jwt.decode(
        token, key=load_key,
        claims_options=claims_options,
        claims_params=claims_params
    )
    return claims.validate(leeway=leeway)


def tmp_password_generator():
    all = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.sample(all, 50))


def validate_token_and_get_user_info(client, bearer_auth):

    if not bearer_auth:
        return None

    auth_token = bearer_auth.replace('Bearer ', '')

    # TODO: properly introspect the token with introspection_endpoint
    # when client introspection is supported by authlib. For now we
    # are just confirming the validity of the claims with the client
    # to ensure someone is not using Oauth tokens issued by another app
    validate_token(client, auth_token)

    structured_token = {
      'access_token': auth_token
    }

    userinfo = client.userinfo(token=structured_token)
    return userinfo


@open_id_blueprint.route('/<provider>/token-exchange/login')
def exchange_login(provider):
    """
    Providing an access_token bearer (eg. acquired by an SPA via PKCE)
    in the Authorization header, make a call to the Openid connect identity
    server requesting information for the user, and return an exchanged token
    for logging in to the rest API
    """
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"msg": "Unsupported"}), 400

    userinfo = validate_token_and_get_user_info(
        client,
        request.headers.get('Authorization')
    )

    if not userinfo or not userinfo['email']:
        return jsonify({"msg": "Insufficient data"}), 400

    user = User.query.filter_by(email=userinfo['email']).one_or_none()

    if user is None:
        return jsonify({"msg": "Bad credentials"}), 400

    result = build_login_success_response(user)

    return jsonify(result), 200


@open_id_blueprint.route('/<provider>/token-exchange/register')
def exchange_register(provider):
    """
    Providing an access_token bearer (eg. acquired by an SPA via PKCE)
    in the Authorization header, make a call to the Openid connect identity
    server requesting information for the user, and return an exchanged token
    for logging in to the rest API
    """
    client = oauth.create_client(provider)
    if not client:
        return jsonify({"msg": "Unsupported"}), 400

    userinfo = validate_token_and_get_user_info(
        client,
        request.headers.get('Authorization')
    )

    if not userinfo or not userinfo['email']:
        return jsonify({"msg": "Insufficient data"}), 400

    user = User.query.filter_by(email=userinfo['email']).one_or_none()

    if user is not None:
        return jsonify({"msg": "User already exists"}), 409

    # Additional properties that can be used (depending on the provider)
    # eg. 'given_name', 'family_name', 'nickname', 'locale'
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
