import datetime
from datetime import timedelta

from fastapi.testclient import TestClient

from app.api import api
from app.model.user_models import RegisterUserRequest
from app.services.user_service import create_access_token

client = TestClient(api)


def test_register_new_accont(fake_user):
    test_username = "user"
    test_password = "pass"
    body = RegisterUserRequest(username=test_username, password=test_password)
    res = client.post("/user/register", body.json())

    payload_token = {
        "sub": test_username,
        "exp": datetime.datetime.utcnow() + timedelta(minutes=30),
    }

    assert res.status_code == 200
    assert res.json()["access_token"] == create_access_token(data=payload_token)
    assert res.json()["token_type"] == "bearer"


def test_register_existing_username(fake_user):
    user, jwt, password = fake_user
    test_username = user["username"]
    test_password = password
    body = RegisterUserRequest(username=test_username, password=test_password)
    res = client.post("/user/register", body.json())

    assert res.status_code == 409
    assert res.json() == {"detail": "User already exists"}
