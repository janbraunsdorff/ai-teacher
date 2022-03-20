import datetime
import json

from fastapi.testclient import TestClient
from mongomock import ObjectId

from app.api import api
from app.database import collections
from app.model.document import Document, Task, TaskType
from app.model.project_model import Class, Project
from app.services.import_service import import_and_convert_to_default
from tests.helper.demo_data import inser_project

client = TestClient(api)


def test_get_targets_no_presents(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user)[0]["id"]

    res = client.get(
        f"/project/{pid}/reuslt-object",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 0


def test_get_targets_one_task_zero_classes_bb(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user, tasks=[TaskType.IMAGE_BOUNDINGBOX])[0]["id"]

    res = client.get(
        f"/project/{pid}/reuslt-object",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == TaskType.IMAGE_BOUNDINGBOX.value
    assert res.json()[0]["id"] == TaskType.IMAGE_BOUNDINGBOX.name


def test_get_targets_one_task_one_classes_bb(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(
        user,
        tasks=[TaskType.IMAGE_BOUNDINGBOX],
        img_bounding_box_classes=[Class(name="name A", describtion="des A")],
    )[0]["id"]

    res = client.get(
        f"/project/{pid}/reuslt-object",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == TaskType.IMAGE_BOUNDINGBOX.value
    assert res.json()[0]["id"] == TaskType.IMAGE_BOUNDINGBOX.name
    assert len(res.json()[0]["targets"]) == 1
    assert res.json()[0]["targets"][0]["name"] == "name A"
    assert res.json()[0]["targets"][0]["describtion"] == "des A"


def test_get_targets_one_task_zero_classes_cls(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user, tasks=[TaskType.IMAGE_CLASSIFICATION])[0]["id"]

    res = client.get(
        f"/project/{pid}/reuslt-object",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == TaskType.IMAGE_CLASSIFICATION.value
    assert res.json()[0]["id"] == TaskType.IMAGE_CLASSIFICATION.name


def test_get_targets_one_task_one_classes_cls(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(
        user,
        tasks=[TaskType.IMAGE_CLASSIFICATION],
        img_classes=[Class(name="name A", describtion="des A")],
    )[0]["id"]

    res = client.get(
        f"/project/{pid}/reuslt-object",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == TaskType.IMAGE_CLASSIFICATION.value
    assert res.json()[0]["id"] == TaskType.IMAGE_CLASSIFICATION.name
    assert len(res.json()[0]["targets"]) == 1
    assert res.json()[0]["targets"][0]["name"] == "name A"
    assert res.json()[0]["targets"][0]["describtion"] == "des A"


def test_get_targets_one_task_zero_classes_ext(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user, tasks=[TaskType.IMAGE_EXTRACTION])[0]["id"]

    res = client.get(
        f"/project/{pid}/reuslt-object",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == TaskType.IMAGE_EXTRACTION.value
    assert res.json()[0]["id"] == TaskType.IMAGE_EXTRACTION.name


def test_get_targets_one_task_one_classes_ext(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(
        user,
        tasks=[TaskType.IMAGE_EXTRACTION],
        img_entities=[Class(name="name A", describtion="des A")],
    )[0]["id"]

    res = client.get(
        f"/project/{pid}/reuslt-object",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == TaskType.IMAGE_EXTRACTION.value
    assert res.json()[0]["id"] == TaskType.IMAGE_EXTRACTION.name
    assert len(res.json()[0]["targets"]) == 1
    assert res.json()[0]["targets"][0]["name"] == "name A"
    assert res.json()[0]["targets"][0]["describtion"] == "des A"


def _test_add_tareget_to_project_bb(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user, tasks=[TaskType.IMAGE_BOUNDINGBOX])[0]["id"]

    res = client.post(
        f"/project/{pid}/add-target",
        json.dumps(
            {
                "task": TaskType.IMAGE_BOUNDINGBOX.name,
                "name": "demo A",
                "describtion": "demo des",
            }
        ),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    project = Project.convert_from_mongo(
        collections["project"].find_one({"_id": ObjectId(pid)})
    )
    assert len(project.img_bounding_box_classes) == 1
    assert project.img_bounding_box_classes[0].name == "demo A"
    assert project.img_bounding_box_classes[0].describtion == "demo des"


def _test_add_tareget_to_project_cls(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user, tasks=[TaskType.IMAGE_CLASSIFICATION])[0]["id"]

    res = client.post(
        f"/project/{pid}/add-target",
        json.dumps(
            {
                "task": TaskType.IMAGE_CLASSIFICATION.name,
                "name": "demo A",
                "describtion": "demo des",
            }
        ),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    project = Project.convert_from_mongo(
        collections["project"].find_one({"_id": ObjectId(pid)})
    )
    assert len(project.img_classes) == 1
    assert project.img_classes[0].name == "demo A"
    assert project.img_classes[0].describtion == "demo des"


def _test_add_tareget_to_project_ext(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user, tasks=[TaskType.IMAGE_EXTRACTION])[0]["id"]

    res = client.post(
        f"/project/{pid}/add-target",
        json.dumps(
            {
                "task": TaskType.IMAGE_EXTRACTION.name,
                "name": "demo A",
                "describtion": "demo des",
            }
        ),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    project = Project.convert_from_mongo(
        collections["project"].find_one({"_id": ObjectId(pid)})
    )
    assert len(project.img_entities) == 1
    assert project.img_entities[0].name == "demo A"
    assert project.img_entities[0].describtion == "demo des"


def _test_add_tareget_to_project_bb(fake_user):
    user, jwt, _ = fake_user
    pid = inser_project(user, tasks=[TaskType.IMAGE_BOUNDINGBOX])[0]["id"]
    import_and_convert_to_default("./tests/assets/import/one_image/", pid)

    res = client.post(
        f"/project/{pid}/add-target",
        json.dumps(
            {
                "task": TaskType.IMAGE_BOUNDINGBOX.name,
                "name": "demo A",
                "describtion": "demo des",
            }
        ),
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200

    doc = Document.convert_from_mongo(
        collections["document"].find_one({"project": pid})
    ).tasks[0]
    assert len(doc.classes) == 1
    assert doc.classes[0].name == "demo A"
    assert doc.classes[0].description == "description"


def _test_add_tareget_to_project_ext():
    assert False


def _test_add_target_to_document():
    assert False
