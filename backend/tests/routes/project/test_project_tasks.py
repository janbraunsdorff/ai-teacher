import datetime
import json

from fastapi.testclient import TestClient
from mongomock import ObjectId

from app.api import api
from app.database import collections
from app.model.document import TaskType
from app.model.project_model import Project

client = TestClient(api)


def test_tasks_no_selected(fake_user):
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
        f"/project/{str(project_ids.inserted_ids[0])}/tasks",
        headers={"Authorization": f"bearer {jwt}"},
    )

    val = res.json()
    assert res.status_code == 200
    assert len(val) == 3
    assert val[0] == {
        "name": TaskType.IMAGE_BOUNDINGBOX.value,
        "id": TaskType.IMAGE_BOUNDINGBOX.name,
        "type": "Images",
        "selected": False,
    }
    assert val[1] == {
        "name": TaskType.IMAGE_CLASSIFICATION.value,
        "id": TaskType.IMAGE_CLASSIFICATION.name,
        "type": "Images",
        "selected": False,
    }
    assert val[2] == {
        "name": TaskType.IMAGE_EXTRACTION.value,
        "id": TaskType.IMAGE_EXTRACTION.name,
        "type": "Images",
        "selected": False,
    }


def test_tasks_one_selected(fake_user):
    user, jwt, _ = fake_user
    time = int(datetime.datetime.utcnow().timestamp() * 1000)

    projects = [
        Project(
            name="p1",
            owner=user["alias"],
            created=time,
            tasks=[TaskType.IMAGE_BOUNDINGBOX],
            img_bounding_box_classes=[],
            img_classes=[],
            img_entities=[],
        ).dict()
    ]

    project_ids = collections["project"].insert_many(projects)

    res = client.get(
        f"/project/{str(project_ids.inserted_ids[0])}/tasks",
        headers={"Authorization": f"bearer {jwt}"},
    )

    val = res.json()
    assert res.status_code == 200
    assert len(val) == 3
    assert val[0] == {
        "name": TaskType.IMAGE_BOUNDINGBOX.value,
        "id": TaskType.IMAGE_BOUNDINGBOX.name,
        "type": "Images",
        "selected": True,
    }
    assert val[1] == {
        "name": TaskType.IMAGE_CLASSIFICATION.value,
        "id": TaskType.IMAGE_CLASSIFICATION.name,
        "type": "Images",
        "selected": False,
    }
    assert val[2] == {
        "name": TaskType.IMAGE_EXTRACTION.value,
        "id": TaskType.IMAGE_EXTRACTION.name,
        "type": "Images",
        "selected": False,
    }


def test_toggle_on_task(fake_user):
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

    res = client.post(
        f"/project/{str(project_ids.inserted_ids[0])}/toggle-task",
        json.dumps({"task_id": TaskType.IMAGE_BOUNDINGBOX.name}),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    project = Project.convert_from_mongo(
        collections["project"].find_one(
            {"_id": ObjectId(str(project_ids.inserted_ids[0]))}
        )
    )
    assert len(project.tasks) == 1
    assert project.tasks[0] == TaskType.IMAGE_BOUNDINGBOX.value


def test_toggle_on_task_with_result(fake_user):
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

    res = client.post(
        f"/project/{str(project_ids.inserted_ids[0])}/toggle-task",
        json.dumps({"task_id": TaskType.IMAGE_BOUNDINGBOX.name}),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    res = client.get(
        f"/project/{str(project_ids.inserted_ids[0])}/tasks",
        headers={"Authorization": f"bearer {jwt}"},
    )

    val = res.json()
    assert res.status_code == 200
    assert len(val) == 3
    assert val[0] == {
        "name": TaskType.IMAGE_BOUNDINGBOX.value,
        "id": TaskType.IMAGE_BOUNDINGBOX.name,
        "type": "Images",
        "selected": True,
    }
    assert val[1] == {
        "name": TaskType.IMAGE_CLASSIFICATION.value,
        "id": TaskType.IMAGE_CLASSIFICATION.name,
        "type": "Images",
        "selected": False,
    }
    assert val[2] == {
        "name": TaskType.IMAGE_EXTRACTION.value,
        "id": TaskType.IMAGE_EXTRACTION.name,
        "type": "Images",
        "selected": False,
    }


def test_toggle_off_task(fake_user):
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

    for i in range(2):
        res = client.post(
            f"/project/{str(project_ids.inserted_ids[0])}/toggle-task",
            json.dumps({"task_id": TaskType.IMAGE_BOUNDINGBOX.name}),
            headers={"Authorization": f"bearer {jwt}"},
        )

        assert res.status_code == 200

    project = Project.convert_from_mongo(
        collections["project"].find_one(
            {"_id": ObjectId(str(project_ids.inserted_ids[0]))}
        )
    )
    assert len(project.tasks) == 0
