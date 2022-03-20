from asyncio import tasks
from pydoc import doc

import pytest

from app.database import collections
from app.model.document import Document, DocumentType, TaskType
from app.services.import_service import import_and_convert_to_default
from tests.helper.demo_data import inser_project, insert_user


@pytest.mark.parametrize(
    "path,num_docs",
    [
        ("./tests/assets/import/one_image/", 1),
        ("./tests/assets/import/one_pdf/", 1),
    ],
)
def test_import_one_image_no_tasks_one_page(patch_mongodb, path, num_docs):
    user = insert_user()
    projects = inser_project(user)
    import_and_convert_to_default(path, projects[0]["id"])

    document = Document.convert_from_mongo(
        collections["document"].find_one({"project": projects[0]["id"]})
    )

    assert document.type == DocumentType.IMAGE.value
    assert len(document.files) == num_docs
    assert document.num_result == 1
    assert len(document.tasks) == 0


@pytest.mark.parametrize(
    "path,num_pages",
    [
        ("./tests/assets/import/many_pages_pdf/", 2),
    ],
)
def test_import_one_image_no_tasks_many_page(patch_mongodb, path, num_pages):
    user = insert_user()
    projects = inser_project(user)
    import_and_convert_to_default(path, projects[0]["id"])

    document = Document.convert_from_mongo(
        collections["document"].find_one({"project": projects[0]["id"]})
    )

    assert document.type == DocumentType.IMAGE.value
    assert len(document.files) == num_pages
    assert document.num_result == 1
    assert len(document.tasks) == 0


@pytest.mark.parametrize(
    "path,num_docs",
    [
        ("./tests/assets/import/many_image/", 3),
    ],
)
def test_import_many_image_no_tasks_one_page(patch_mongodb, path, num_docs):
    user = insert_user()
    projects = inser_project(user)
    import_and_convert_to_default(path, projects[0]["id"])

    document = list(
        collections["document"].find({"project": projects[0]["id"]})
    )

    assert len(document) == num_docs


@pytest.mark.parametrize(
    "path,num_docs",
    [
        ("./tests/assets/import/one_image/", 1),
        ("./tests/assets/import/one_pdf/", 1),
    ],
)
def test_import_one_image_with_Task_tasks_one_page(
    patch_mongodb, path, num_docs
):
    user = insert_user()
    classes = ["class A", "class B"]
    projects = inser_project(
        user,
        classes=[
            {"name": "class A", "describtion": "desc A"},
            {"name": "class B", "describtion": "desc B"},
        ],
        tasks=[
            TaskType.IMAGE_BOUNDINGBOX,
            TaskType.IMAGE_CLASSIFICATION,
            TaskType.IMAGE_EXTRACTION,
        ],
    )
    import_and_convert_to_default(path, projects[0]["id"])

    document = Document.convert_from_mongo(
        collections["document"].find_one({"project": projects[0]["id"]})
    )

    print(document)

    assert document.type == DocumentType.IMAGE.value
    assert len(document.files) == num_docs
    assert document.num_result == 1
    assert len(document.tasks) == 3

    assert document.tasks[0].type == TaskType.IMAGE_BOUNDINGBOX.value
    assert len(document.tasks[0].results) == 0
    assert (
        len(
            [item for item in document.tasks[0].entities if item not in classes]
        )
        == 0
    )

    assert document.tasks[1].type == TaskType.IMAGE_CLASSIFICATION.value
    assert len(document.tasks[1].results) == 0
    assert (
        len([item for item in document.tasks[1].classes if item not in classes])
        == 0
    )

    assert document.tasks[2].type == TaskType.IMAGE_EXTRACTION.value
    assert len(document.tasks[2].results) == 0
    assert (
        len(
            [item for item in document.tasks[2].entities if item not in classes]
        )
        == 0
    )
