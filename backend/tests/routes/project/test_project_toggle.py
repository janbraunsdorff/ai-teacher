import datetime
from datetime import datetime as dt

from fastapi.testclient import TestClient
from mongomock import ObjectId

from app.api import api
from app.database import collections
from app.model.project_model import (
    CreateProject,
    Project,
    ProjectHeader,
    ToggleWorkerRequest,
)
from app.model.user_models import User
from tests.helper.demo_data import inser_project

client = TestClient(api)


def test_toggle_worker_on(fake_user):
    user, jwt, _ = fake_user
    project = inser_project(user)[0]

    res = client.post(
        f"/project/{project['id']}/toggle-worker",
        ToggleWorkerRequest(worker_id=user["id"]).json(),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    user = User(**collections["user"].find_one({"_id": ObjectId(user["id"])}))
    assert project["id"] in user.working_on


def test_toggle_worker_off(fake_user):
    user, jwt, _ = fake_user
    project = inser_project(user)[0]

    for _ in range(2):
        res = client.post(
            f"/project/{project['id']}/toggle-worker",
            ToggleWorkerRequest(worker_id=user["id"]).json(),
            headers={"Authorization": f"bearer {jwt}"},
        )
        assert res.status_code == 200

    user = User(**collections["user"].find_one({"_id": ObjectId(user["id"])}))
    assert project["id"] not in user.working_on


def test_toggle_worker_not_athorized(fake_user):
    user, jwt, _ = fake_user
    project = inser_project({"alias": "abc"})[0]

    res = client.post(
        f"/project/{project['id']}/toggle-worker",
        ToggleWorkerRequest(worker_id=user["id"]).json(),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 403
