
from flask import url_for


# GET
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


# DELETE
def test_user_cannot_delete_own_details(client, common_user, user_headers):
    # User triest to access their own details
    user_url = url_for('api.users.UserById', user_id=common_user.id)
    rep = client.delete(user_url, headers=user_headers)
    assert rep.status_code == 401


def test_user_cannot_delete_others_details(client, user_headers, admin_user):
    # User tries to access admin user details
    user_url = url_for('api.users.UserById', user_id=admin_user.id)
    rep = client.delete(user_url, headers=user_headers)
    assert rep.status_code == 401


# PUT
def test_user_can_edit_their_own_details(client, common_user, user_headers):
    # User triest to access their own details
    user_url = url_for('api.users.UserById', user_id=common_user.id)
    data = {"email": "updated@email.com"}
    rep = client.put(user_url, json=data, headers=user_headers)
    assert rep.status_code == 200

    data = rep.get_json()
    assert data["email"] == common_user.email


def test_user_cannot_edit_others_details(client, user_headers, admin_user):
    # User tries to update admin user details
    user_url = url_for('api.users.UserById', user_id=admin_user.id)
    data = {"email": "updated@email.com"}
    rep = client.put(user_url, json=data, headers=user_headers)
    assert rep.status_code == 401


# GET USERS
def test_user_can_list_limited_users(client, common_user, admin_user, user_headers):
    # User triest to access their own details
    user_url = url_for('api.users.Users')
    rep = client.get(user_url, headers=user_headers)
    assert rep.status_code == 200

    data = rep.get_json()
    assert len(data) == 1
    response_ids = [response_user["id"] for response_user in data]
    assert admin_user.id not in response_ids
    assert common_user.id in response_ids

