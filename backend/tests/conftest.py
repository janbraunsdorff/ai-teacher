import datetime
import sys
from datetime import timedelta

import pytest
from jose import jwt

import app.services.user_service as us

FAKE_TIME = datetime.datetime.utcnow()


@pytest.fixture
def freeze_time(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

        @classmethod
        def utcnow(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, "datetime", mydatetime)


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer


@pytest.fixture
def patch_security(monkeypatch):
    us.SECRET_KEY = "myTopSecretKey"
    monkeypatch.setattr(us, "SECRET_KEY", "myTopSecretKey")


@pytest.fixture
def fake_user(monkeypatch, patch_security, freeze_time):
    password = "test_password"
    username = "test_username"

    user = {
        "username": username,
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": us.get_password_hash(password),
        "disabled": False,
    }
    monkeypatch.setitem(us.fake_users_db, username, user)

    to_encode = {"sub": user["username"]}
    to_encode.update(
        {"exp": datetime.datetime.utcnow() + timedelta(minutes=30)}
    )
    encoded_jwt = jwt.encode(to_encode, us.SECRET_KEY, algorithm=us.ALGORITHM)

    yield (user, encoded_jwt, password)
