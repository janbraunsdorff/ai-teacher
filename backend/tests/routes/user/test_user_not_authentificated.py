from fastapi.testclient import TestClient

from app.api import api

client = TestClient(api)


def test_login_wrong_credentials(fake_user):
    res = client.post(
        url="/user/login", data={"username": "wrong", "password": "user"}
    )
    assert res.status_code == 401


def test_self_wrong_credentials(fake_user):
    res = client.post(
        url="/user/login", data={"username": "wrong", "password": "user"}
    )
    assert res.status_code == 401


def test_self_no_credentials(fake_user):
    res = client.post(
        url="/user/login", data={"username": "wrong", "password": "user"}
    )
    assert res.status_code == 401
