import json

from fastapi.testclient import TestClient

from app.api import api
from app.database import collections
from app.model.document import Document, TaskType
from app.services.import_service import import_and_convert_to_default
from tests.helper.demo_data import inser_project

client = TestClient(api)


def test_update_existing_tasks_in_documents_add(fake_user):
    user, jwt, _ = fake_user
    projects = inser_project(user)
    import_and_convert_to_default(
        "./tests/assets/import/many_image/", projects[0]["id"]
    )

    client.post(
        f"/project/{projects[0]['id']}/toggle-task",
        json.dumps({"task_id": TaskType.IMAGE_BOUNDINGBOX.name}),
        headers={"Authorization": f"bearer {jwt}"},
    )

    documents = collections["document"].find({"project": projects[0]["id"]})
    for doc in documents:
        doc = Document.convert_from_mongo(doc)
        assert len(doc.tasks) == 1
        assert doc.tasks[0].type == TaskType.IMAGE_BOUNDINGBOX.value
        assert doc.tasks[0].results == []
        assert doc.tasks[0].entities == []
