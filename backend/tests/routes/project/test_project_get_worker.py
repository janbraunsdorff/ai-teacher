import datetime
from datetime import datetime as dt

from fastapi.testclient import TestClient

from app.api import api
from app.database import collections
from app.model.project_model import CreateProject, Project, ProjectHeader

client = TestClient(api)


def test_get_all_worker_no_worker_is_in(fake_user):
    user, jwt, _ = fake_user
    time = int(datetime.datetime.utcnow().timestamp() * 1000)

    projects = [
        Project(
            name="p1", owner=user["alias"], created=time, tasks=[], classes=[]
        ).dict()
    ]
    project_ids = collections["project"].insert_many(projects)

    res = client.get(
        f"/project/{str(project_ids.inserted_ids[0])}/worker",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == {
        "alias": user["alias"],
        "id": str(user["_id"]),
        "is_worker": False,
        "name": user["name"],
    }


def test_get_all_worker_one_worker_is_in(fake_user):
    user, jwt, _ = fake_user
    time = int(datetime.datetime.utcnow().timestamp() * 1000)

    projects = [
        Project(
            name="p1", owner=user["alias"], created=time, tasks=[], classes=[]
        ).dict()
    ]
    project_ids = collections["project"].insert_many(projects)
    collections["user"].update_one(
        filter={"alias": user["alias"]},
        update={"$push": {"working_on": str(project_ids.inserted_ids[0])}},
    )

    res = client.get(
        f"/project/{str(project_ids.inserted_ids[0])}/worker",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == {
        "alias": user["alias"],
        "id": str(user["_id"]),
        "is_worker": True,
        "name": user["name"],
    }


# TODO- (one, one out) (one has other) (one has other an current)
