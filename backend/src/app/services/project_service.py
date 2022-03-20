import base64
import datetime
import io
from typing import List, Union

from fastapi import HTTPException, status
from PIL import Image

import app.database.user as user_database
from app.database import project
from app.database.document import (
    find_all_imanges_by_project,
    push_class_document,
    update_tasks,
)
from app.database.project import (
    all,
    get_by_id,
    insert_project,
    push_class_project,
    toggle_active_tasks,
)
from app.model.document import (
    ImageBoundingBoxTask,
    ImageClassificationTask,
    ImageExtractionTask,
    Task,
    TaskType,
)
from app.model.project_model import (
    Class,
    ImageMeta,
    PossibleTask,
    Project,
    ProjectHeader,
    ResultObjectRespnse,
    TaskShort,
    Worker,
)
from app.model.user_models import User
from app.services import convert_timestamp


def get_project_header():
    return [
        ProjectHeader(
            id=project.id,
            name=project.name,
            created=convert_timestamp(project.created),
        )
        for project in all()
    ]


def create_project(project: Project, user: User):
    project = Project(
        name=project.name,
        owner=user.alias,
        created=datetime.datetime.utcnow().timestamp() * 1000,
        tasks=[],
        img_entities=[],
        img_bounding_box_classes=[],
        img_classes=[],
    )
    insert_project(project=project)


def get_worker(pid: str):
    return [
        Worker(
            id=str(x["_id"]),
            name=x["name"],
            is_worker=x["is_worker"],
            alias=x["alias"],
        )
        for x in user_database.get_worker_for_project(pid=pid)
    ]


def toggle_user(pid: str, wid: str, current_user: User):
    user_database.togel_project(wid, pid)


def check_for_project_owner(current_user: User, pid: str):
    project = get_by_id(pid)
    if project.owner != current_user.alias:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid permissions",
        )


def get_images(pid):
    docs = find_all_imanges_by_project(pid)
    res = []
    for doc in docs:
        name = doc.id
        img = base64.b64decode(doc.files[0])
        shape = str(Image.open(io.BytesIO(img)).size)
        tasks = prettify_tasks(doc.tasks)
        res.append(ImageMeta(name=name, shape=shape, tasks=tasks))
    return res


def prettify_tasks(tasks: List[Task]) -> List[TaskShort]:
    return [TaskShort(name=x.type, done=False) for x in tasks]


def get_tasks(pid):
    project = get_by_id(pid)
    return [
        PossibleTask(
            name=task.value,
            id=task.name,
            type="Images",
            selected=task.value in project.tasks,  # type: ignore
        )
        for task in TaskType
    ]


def toggle_task(pid: str, task_id: str):
    toggle_active_tasks(pid, task_id)
    project = get_by_id(pid)
    tasks = []
    for task in project.tasks:
        task = TaskType(task)
        if task == TaskType.IMAGE_BOUNDINGBOX:
            tasks.append(
                ImageBoundingBoxTask(
                    type=task,
                    results=[],
                    targets=[],
                    entities=[x.name for x in project.img_bounding_box_classes],
                )
            )
        if task == TaskType.IMAGE_CLASSIFICATION:
            tasks.append(
                ImageClassificationTask(
                    type=task,
                    results=[],
                    targets=[],
                    classes=[x.name for x in project.img_classes],
                )
            )
        if task == TaskType.IMAGE_EXTRACTION:
            tasks.append(
                ImageExtractionTask(
                    type=task,
                    results=[],
                    targets=[],
                    entities=[x.name for x in project.img_entities],
                )
            )

    update_tasks(pid, [task.dict() for task in tasks])


def getResultObjects(pid: str):
    project = get_by_id(pid)
    tasks = []
    for task in project.tasks:
        task = TaskType(task)
        tasks.append(
            ResultObjectRespnse(
                name=task.value,
                id=task.name,
                targets=get_targets(task, project),
            )
        )
    return tasks


def get_targets(task, project: Project):
    conf = {
        TaskType.IMAGE_BOUNDINGBOX: "img_bounding_box_classes",
        TaskType.IMAGE_EXTRACTION: "img_entities",
        TaskType.IMAGE_CLASSIFICATION: "img_classes",
    }
    return project.dict()[conf.get(task, "")]


def add_target(pid: str, task: str, name: str, describtion: str):
    conf = {
        TaskType.IMAGE_BOUNDINGBOX: "img_bounding_box_classes",
        TaskType.IMAGE_EXTRACTION: "img_entities",
        TaskType.IMAGE_CLASSIFICATION: "img_classes",
    }
    push_class_project(
        pid,
        conf.get(TaskType[task]),
        Class(name=name, describtion=describtion).dict(),
    )

    push_class_document(
        pid,
        TaskType[task].value,
        Class(name=name, describtion=describtion).dict(),
    )
