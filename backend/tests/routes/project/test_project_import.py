import datetime

from fastapi.testclient import TestClient

from app.api import api
from app.database import collections
from app.model.project_model import ImportRequest
from tests.helper.demo_data import inser_project

client = TestClient(api)


def test_import_invalid_permissions(fake_user):
    user, jwt, _ = fake_user

    pid = inser_project({"alias": "abc"})[0]["id"]

    res = client.post(
        f"/project/{pid}/import",
        ImportRequest(path="").json(),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 403


def test_import_valid_path(fake_user):
    user, jwt, _ = fake_user

    pid = inser_project(user)[0]["id"]

    res = client.post(
        f"/project/{pid}/import",
        ImportRequest(path="./tests/assets/import/many_image/").json(),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert res.json()["num_imported"] == 3
    assert res.json()["error_files"] == []


def test_import_invalid_path(fake_user):
    user, jwt, _ = fake_user

    pid = inser_project(user)[0]["id"]

    res = client.post(
        f"/project/{pid}/import",
        ImportRequest(path="./tests/assets/import/not_existing/").json(),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 404
