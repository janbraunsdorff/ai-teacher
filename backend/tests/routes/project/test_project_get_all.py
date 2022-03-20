import datetime
from datetime import datetime as dt

from fastapi.testclient import TestClient

from app.api import api
from app.database import collections
from app.model.project_model import CreateProject, Project, ProjectHeader

client = TestClient(api)


def test_get_all_projects_one(fake_user):
    user, jwt, _ = fake_user
    time = int(datetime.datetime.utcnow().timestamp() * 1000)

    projects = [
        Project(
            name="p1",
            owner=user["alias"],
            created=time,
            tasks=[],
            img_bounding_box_classes=[],
            img_classes=[],
            img_entities=[],
        ).dict()
    ]

    project_ids = collections["project"].insert_many(projects)

    res = client.get(
        "/project/all",
        headers={"Authorization": f"bearer {jwt}"},
    )

    res = [ProjectHeader(**pro) for pro in res.json()]

    assert len(res) == 1
    assert res[0].id == str(project_ids.inserted_ids[0])
    assert res[0].name == "p1"
    assert res[0].created == dt.utcfromtimestamp(time / 10000).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
