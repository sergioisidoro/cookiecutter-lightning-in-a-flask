import json
import datetime
from flask import url_for
from freezegun import freeze_time


def test_invalid_login_request(client, common_user):
    data = {
        'email': common_user.email,
    }
    resp = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )
    assert resp.status_code == 400

    data = {
        'password': "Hunter2",
    }
    resp = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )
    assert resp.status_code == 400

    data = "This!Is;Totally!notJSON"
    resp = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )
    assert resp.status_code == 400


def test_invalid_login(client, db):
    data = {
        'email': 'This@doesnt.exist',
        'password': "Hunter2",
    }
    resp = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )
    assert resp.status_code == 400


def test_expiry_and_refresh(client, app, admin_user):
    data = {
        'email': admin_user.email,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    access_token = tokens['access_token']
    refres_token = tokens['refresh_token']
    admin_headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % access_token
    }

    refresh_headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % refres_token
    }

    # everything works
    user_url = url_for('api.users.UserById', user_id=admin_user.id)
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 200

    now = datetime.datetime.now()
    future = now + app.config["JWT_ACCESS_TOKEN_EXPIRES"] + \
        datetime.timedelta(seconds=10)

    far_future = now + app.config["JWT_REFRESH_TOKEN_EXPIRES"] + \
        datetime.timedelta(seconds=10)

    with freeze_time(now) as frozen_datetime:
        frozen_datetime.move_to(future)
        # Auth token expired
        test_response = client.get(user_url, headers=admin_headers)
        assert test_response.status_code == 401

        # Refreshing works
        refresh_response = client.post(
            "/auth/refresh",
            headers=refresh_headers
        )
        assert refresh_response.status_code == 200

        new_token = json.loads(refresh_response.get_data(as_text=True))
        admin_headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer %s' % new_token['access_token']
        }

        new_test_response = client.get(user_url, headers=admin_headers)
        assert new_test_response.status_code == 200

        # Move to a time where Refresh token is expired
        frozen_datetime.move_to(far_future)
        refresh_response = client.post(
            "/auth/refresh",
            headers=refresh_headers
        )
        # Cannot refresh
        assert refresh_response.status_code == 401


def test_revoke_access_token(client, admin_headers):
    resp = client.delete("/auth/revoke_access", headers=admin_headers)
    assert resp.status_code == 200

    resp = client.get("/api/v1/users/1", headers=admin_headers)
    assert resp.status_code == 401


def test_revoke_refresh_token(client, admin_refresh_headers):
    resp = client.delete("/auth/revoke_refresh", headers=admin_refresh_headers)
    assert resp.status_code == 200

    resp = client.post("/auth/refresh", headers=admin_refresh_headers)
    assert resp.status_code == 401


def test_cannot_refresh_revoked_token(client, admin_user):
    data = {
        'email': admin_user.email,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    access_token = tokens['access_token']
    refres_token = tokens['refresh_token']
    admin_headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % access_token
    }

    refresh_headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % refres_token
    }

    refresh_response = client.post("/auth/refresh", headers=refresh_headers)
    assert refresh_response.status_code == 200

    new_token = json.loads(refresh_response.get_data(as_text=True))
    admin_headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % new_token['access_token']
    }

    resp = client.delete("/auth/revoke_access", headers=admin_headers)
    assert resp.status_code == 200

    resp = client.post("/auth/refresh", headers=refresh_headers)
    assert resp.status_code == 401
