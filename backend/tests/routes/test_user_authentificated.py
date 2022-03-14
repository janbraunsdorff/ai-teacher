import json

from fastapi.testclient import TestClient

import app.services.user_service as us
from app.api import api

client = TestClient(api)


def test_patches(fake_user):
    user, _, _ = fake_user
    assert user["username"] in us.fake_users_db
    assert us.SECRET_KEY == "myTopSecretKey"


def test_login(fake_user):
    user, jwt, password = fake_user
    res = client.post(
        "/user/login", {"username": user["username"], "password": password}
    )
    assert res.status_code == 200
    assert res.json()["access_token"] == jwt
    assert res.json()["token_type"] == "bearer"


def test_get_self(fake_user):
    user, jwt, _ = fake_user
    res = client.get("/user/self", headers={"Authorization": f"bearer {jwt}"})

    del user["hashed_password"]
    assert res.status_code == 200
    assert res.json() == json.loads(json.dumps(user))
