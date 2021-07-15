from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from bottle.models import User
from bottle.extensions import pwd_context, jwt
from bottle.auth.helpers import (
  revoke_token,
  revoke_refresh_token,
  is_token_revoked,
  create_session_and_session_token,
  refresh_session
)

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json or isinstance(request.json, str):
        return jsonify({"msg": "Not a JSON in request"}), 400

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).one_or_none()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Bad credentials"}), 400

    (access_token, refresh_token) = create_session_and_session_token(user)

    result = {
      "user_id": user.id,
      "access_token": access_token,
      "refresh_token": refresh_token
    }
    return jsonify(result), 200


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    jti = get_jwt()["jti"]
    current_user = get_jwt_identity()
    access_token = refresh_session(current_user, jti)
    if access_token:
        ret = {"access_token": access_token}
        return jsonify(ret), 200
    else:
        return "Unauthorised", 402


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh():
    jti = get_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_refresh_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_loader_callback(jwt_headers, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query.get(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_headers, jwt_payload)


# @blueprint.before_app_first_request
# def register_views():
#     apispec.spec.path(view=login, app=app)
#     apispec.spec.path(view=refresh, app=app)
#     apispec.spec.path(view=revoke_access_token, app=app)
#     apispec.spec.path(view=revoke_refresh_token, app=app)
