import base64
import datetime
import io
from typing import List, Union

from fastapi import HTTPException, status
from PIL import Image

import app.database.user as user_database
from app.database.document import find_all_imanges_by_project
from app.database.project import (
    all,
    get_by_id,
    insert_project,
    toggle_active_tasks,
)
from app.model.document import Task, TaskType
from app.model.project_model import (
    ImageMeta,
    PossibleTask,
    Project,
    ProjectHeader,
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
