import datetime
import json
from datetime import timedelta

from fastapi.testclient import TestClient

import app.services.user_service as us
from app.api import api

client = TestClient(api)


def test_login_no_existing_user(fake_user):
    user, jwt, password = fake_user
    payload_token = {
        "sub": user["username"],
        "exp": datetime.datetime.utcnow() + timedelta(minutes=30),
    }
    jwt = us.create_access_token(data=payload_token)

    res = client.post(
        "/user/login", {"username": "myUserName", "password": password}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Incorrect username or password"}


def test_login(fake_user):
    user, jwt, password = fake_user
    res = client.post(
        "/user/login", {"username": user["username"], "password": password}
    )
    assert res.status_code == 200
    assert res.json()["access_token"] == jwt
    assert res.json()["token_type"] == "bearer"


def test_login_wrong_password(fake_user):
    user, jwt, password = fake_user
    res = client.post(
        "/user/login", {"username": user["username"], "password": "myPassword"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Incorrect username or password"}


def test_get_self(fake_user):
    user, jwt, _ = fake_user
    res = client.get("/user/self", headers={"Authorization": f"bearer {jwt}"})

    del user["hashed_password"]
    del user["_id"]
    assert res.status_code == 200
    assert res.json() == json.loads(json.dumps(user))


def test_missing_user_name(fake_user):
    user, jwt, _ = fake_user
    payload_token = {
        "exp": datetime.datetime.utcnow() + timedelta(minutes=30),
    }
    jwt = us.create_access_token(data=payload_token)
    res = client.get("/user/self", headers={"Authorization": f"bearer {jwt}"})

    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_wrong_secret_to_encode(fake_user, monkeypatch):
    user, jwt, _ = fake_user

    payload_token = {
        "sub": user["username"],
        "exp": datetime.datetime.utcnow() + timedelta(minutes=30),
    }
    jwt = us.create_access_token(data=payload_token)

    us.SECRET_KEY = "notMyTopSecretKey"
    monkeypatch.setattr(us, "SECRET_KEY", "notMyTopSecretKey")

    res = client.get("/user/self", headers={"Authorization": f"bearer {jwt}"})

    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_valid_token_user_not_exists(fake_user):
    payload_token = {
        "sub": "myUser",
        "exp": datetime.datetime.utcnow() + timedelta(minutes=30),
    }
    jwt = us.create_access_token(data=payload_token)
    res = client.get("/user/self", headers={"Authorization": f"bearer {jwt}"})

    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_valid_token_user_disabled(fake_user_disabled):
    user, jwt, _ = fake_user_disabled
    res = client.get("/user/self", headers={"Authorization": f"bearer {jwt}"})

    assert res.status_code == 400
    assert res.json() == {"detail": "Inactive user"}
