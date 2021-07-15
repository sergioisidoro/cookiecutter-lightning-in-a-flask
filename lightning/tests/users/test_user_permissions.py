
from flask import url_for


def test_user_can_see_their_own_details(client, common_user, user_headers):
    # User triest to access their own details
    user_url = url_for('api.users.UserById', user_id=common_user.id)
    rep = client.get(user_url, headers=user_headers)
    assert rep.status_code == 200

    data = rep.get_json()
    assert data["email"] == common_user.email
    assert data["active"] == common_user.active


def test_user_cannot_see_others_details(client, user_headers, admin_user):
    # User tries to access admin user details
    user_url = url_for('api.users.UserById', user_id=admin_user.id)
    rep = client.get(user_url, headers=user_headers)
    assert rep.status_code == 401
