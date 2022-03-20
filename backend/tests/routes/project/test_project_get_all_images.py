from fastapi.testclient import TestClient

from app.api import api
from app.model.document import TaskType
from app.services.import_service import import_and_convert_to_default
from tests.helper.demo_data import inser_project

client = TestClient(api)


def test_get_images_no_images(fake_user):
    user, jwt, _ = fake_user
    project = inser_project(user)[0]

    res = client.get(
        f"/project/{project['id']}/images",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 0


def test_get_images_meta(fake_user):
    user, jwt, _ = fake_user

    path = "./tests/assets/import/many_image/"
    project = inser_project(
        user,
        img_entities=[
            {"name": "class A", "describtion": "desc A"},
            {"name": "class B", "describtion": "desc B"},
        ],
        img_bounding_box_classes=[
            {"name": "class C", "describtion": "desc A"},
            {"name": "class D", "describtion": "desc B"},
        ],
        img_classes=[
            {"name": "class E", "describtion": "desc A"},
            {"name": "class F", "describtion": "desc B"},
        ],
        tasks=[
            TaskType.IMAGE_BOUNDINGBOX,
            TaskType.IMAGE_CLASSIFICATION,
            TaskType.IMAGE_EXTRACTION,
        ],
    )[0]
    import_and_convert_to_default(path, project["id"])

    res = client.get(
        f"/project/{project['id']}/images",
        headers={"Authorization": f"bearer {jwt}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 3
