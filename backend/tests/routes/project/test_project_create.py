import datetime

from fastapi.testclient import TestClient

from app.api import api
from app.database import collections
from app.model.project_model import CreateProject, Project

client = TestClient(api)


def test_create_project(fake_user):
    user, jwt, _ = fake_user
    test_project_name = "test_project_name"
    res = client.post(
        "/project/create",
        CreateProject(name=test_project_name).json(),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    project = collections["project"].find_one({"owner": user["alias"]})
    project = Project.convert_from_mongo(project)

    assert project.name == test_project_name
    assert project.owner == user["alias"]
    assert project.created == int(datetime.datetime.utcnow().timestamp() * 1000)


def test_create_project_no_auth(fake_user):
    user, jwt, _ = fake_user
    test_project_name = "test_project_name"
    res = client.post(
        "/project/create",
        CreateProject(name=test_project_name).json(),
    )

    assert res.status_code == 401
