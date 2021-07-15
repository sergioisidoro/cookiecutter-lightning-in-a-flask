import json

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

