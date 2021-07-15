
from flask import url_for


# GET
def test_root_url_responds(client):
    # User triest to access their own details
    rep = client.get("/")
    assert rep.status_code == 200
