import pytest
from spending_tracker import db
from spending_tracker.cli import app_maker
import tempfile
import os
from spending_tracker import api, blueprint
from unittest.mock import patch
import json
from spending_tracker.db_models.db_models import UserModel


@pytest.fixture
def test_client():
    app = app_maker()
    db_fd, db_fname = tempfile.mkstemp()

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True
    app.config['SERVER_NAME'] = 'testing.com'

    ctx = app.app_context()
    with ctx:
        db.create_all()
    ctx.push()
    test_app = app.test_client()
    yield test_app

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


def test_get_users(test_client):
    u1 = UserModel(user='user_1', balance=12)
    u2 = UserModel(user='user_2', balance=15)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    rv = test_client.get('/api/users/')
    assert rv.status_code == 200
    assert rv.get_json() == {
      "properties": {
        "user_1": {
          "self": "/api/users/user_1/",
          "wallet": "/api/user/user_1/money/",
          "categories": "/api/categories/user_1/"
        },
        "user_2": {
          "self": "/api/users/user_2/",
          "wallet": "/api/user/user_2/money/",
          "categories": "/api/categories/user_2/"
        }
      }
    }


def test_get_user(test_client):
    u = UserModel(user='user', balance=12)
    db.session.add(u)
    db.session.commit()
    rv = test_client.get('/api/users/user/')
    assert rv.status_code == 200
    assert rv.get_json() == {
      "properties": {
        "user": "user",
        "balance": 12.0
      },
      "links": {
        "self": "/api/users/user/",
        "collection": '/api/users/',
        "wallet": "/api/user/user/money/",
        "categories": "/api/categories/user/"
      }
    }


def test_get_user_fail(test_client):
    rv = test_client.get('/api/users/user/')
    assert rv.status_code == 404


def test_post_user(test_client):
    user = {
        'user': 'tester',
        'balance': 12.0
    }
    rv = test_client.post('/api/users/', json=user)
    assert rv.status_code == 201
    assert rv.headers['Location'] == 'http://testing.com/api/users/tester/'


def test_user_add_money(test_client):
    u = UserModel(user='tester', balance=12)
    db.session.add(u)
    db.session.commit()
    payload = {'money': 123}
    rv = test_client.post('/api/user/tester/money/', json=payload)
    assert rv.status_code == 201


def test_user_add_money_fail(test_client):
    payload = {'money': 123}
    rv = test_client.post('/api/user/tester/money/', json=payload)
    assert rv.status_code == 404


