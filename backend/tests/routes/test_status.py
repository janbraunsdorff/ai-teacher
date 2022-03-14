import pytest
from fastapi.testclient import TestClient

from app.api import api

client = TestClient(api)


def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert isinstance(response.json()["date"], int)
