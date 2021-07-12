import json
import pytest
from dotenv import load_dotenv

from bottle.models import User
from bottle.app import create_app
from bottle.db import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory


register(UserFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv("test.env")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        email='admin@admin.com',
        password='admin',
        admin=True
    )

    db.session.add(user)
    db.session.commit()
    return user
