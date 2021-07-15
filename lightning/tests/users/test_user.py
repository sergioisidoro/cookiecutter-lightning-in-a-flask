from flask import url_for

from bottle.extensions import pwd_context
from bottle.models import User


def test_get_user(client, db, user, admin_headers):
    # test 404
    user_url = url_for('api.users.UserById', user_id="100000")
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    user_url = url_for('api.users.UserById', user_id=user.id)
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()
    assert data["email"] == user.email
    assert data["active"] == user.active


def test_put_user(client, db, user, admin_headers):
    user_url = url_for('api.users.UserById', user_id="100000")
    rep = client.put(user_url, headers=admin_headers)
    assert rep.status_code == 422

    db.session.add(user)
    db.session.commit()

    data = {"email": "updated@email.com", "password": "new_password"}

    user_url = url_for('api.users.UserById', user_id=user.id)
    # test update user
    rep = client.put(user_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()
    assert data["email"] == user.email
    assert data["active"] == user.active

    db.session.refresh(user)

    assert pwd_context.verify("new_password", user.password)


def test_delete_user(client, db, user, admin_headers):
    # test 404
    user_url = url_for('api.users.UserById', user_id="100000")
    rep = client.delete(user_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user

    user_url = url_for('api.users.UserById', user_id=user.id)
    rep = client.delete(user_url,  headers=admin_headers)
    assert rep.status_code == 204
    assert db.session.query(User).filter_by(id=user.id).first() is None


def test_create_user(client, db, admin_headers):
    # test bad data
    users_url = url_for('api.users.Users')
    data = {"email": "created@email.com"}
    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 422

    data["password"] = "admin"
    data["email"] = "create@mail.com"

    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data["id"]).first()

    assert user.email == "create@mail.com"


def test_get_all_user(client, db, user_factory, admin_headers):
    users_url = url_for('api.users.Users')
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    rep = client.get(users_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results)
