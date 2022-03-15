import datetime
from datetime import timedelta

from fastapi.testclient import TestClient

from app.api import api
from app.database import collections
from app.model.user_models import RegisterUserRequest
from app.services.user_service import create_access_token

client = TestClient(api)


def test_register_new_accont(fake_user):
    test_username = "user"
    test_password = "pass"
    body = RegisterUserRequest(
        alias=test_username, password=test_password, name="Jan"
    )
    res = client.post("/user/register", body.json())

    payload_token = {
        "sub": test_username,
        "exp": datetime.datetime.utcnow() + timedelta(minutes=30),
    }

    assert res.status_code == 200
    assert res.json()["access_token"] == create_access_token(data=payload_token)
    assert res.json()["token_type"] == "bearer"


def test_register_new_accont(fake_user):
    test_username = "user2"
    test_password = "pass2"
    body = RegisterUserRequest(
        alias=test_username, password=test_password, name="Jan2"
    )
    client.post("/user/register", body.json())

    user = collections["user"].find_one({"alias": test_username})

    for value in ["alias", "roles", "name", "password", "_id"]:
        assert value in user

    assert user["alias"] == "user2"
    assert user["roles"] == ["worker"]
    assert user["name"] == "Jan2"


def test_register_existing_username(fake_user):
    user, jwt, password = fake_user
    test_username = user["alias"]
    test_password = password
    body = RegisterUserRequest(
        alias=test_username, password=test_password, name="Jan"
    )
    res = client.post("/user/register", body.json())

    assert res.status_code == 409
    assert res.json() == {"detail": "User already exists"}
