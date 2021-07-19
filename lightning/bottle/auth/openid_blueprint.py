from flask import Blueprint, url_for, jsonify, request
from bottle.extensions import oauth
from bottle.auth.helpers import (
  build_login_success_response,
)

open_id_blueprint = Blueprint("oauth", __name__, url_prefix="/oauth")


@open_id_blueprint.route('/<provider>/token-exchange')
def exchange_token(provider):
    client = oauth.create_client('google')
    if not client:
        print("BOO")

    token = request.headers.get('Authorization')
    auth_token = token.replace('Bearer ','')

    

    print(client.introspect_token(auth_token))
    #result = {userinfo}
    # result = build_login_success_response(user)
    result = {}
    return jsonify(result), 200
