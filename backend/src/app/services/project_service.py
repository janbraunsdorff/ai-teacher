import base64
import datetime
import io
from typing import List, Union

from fastapi import HTTPException, status
from PIL import Image

import app.database.user as user_database
from app.database.document import (
    find_all_imanges_by_project,
    push_class_document,
    pull_task,
    delete_task_document,
    push_new_task
)
from app.database.project import (
    all,
    get_by_id,
    insert_project,
    push_class_project,
    toggle_active_tasks,
    delete_class_project
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
    Excercies,
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
        result = extract_results(doc.tasks)
        res.append(
            ImageMeta(
                name=name, 
                shape=shape, 
                tasks=tasks,
                results=result
            )
        )
    return res


def prettify_tasks(tasks: List[Task]) -> List[TaskShort]:
    return [TaskShort(name=x.type, done=len(x.results) >= 1) for x in tasks]

def extract_results(tasks: List[Task]):
    config = {}

    for task in tasks:
        if len(task.results) >= 1:
            config[task.type] = task.results[0]

    return config

    


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
    # TODO delete existing labels by updating
    tasks, to_add = toggle_active_tasks(pid, task_id)
    if to_add:
        project = get_by_id(pid)

        if task_id == TaskType.IMAGE_BOUNDINGBOX.name:
            obj = ImageBoundingBoxTask(
                    type=TaskType.IMAGE_BOUNDINGBOX.value,
                    results=[],
                    targets=project.img_bounding_box_classes,
                    entities=[],
                )
            
        if task_id == TaskType.IMAGE_CLASSIFICATION.name:
            obj = ImageClassificationTask(
                    type=TaskType.IMAGE_CLASSIFICATION.value,
                    results=[],
                    targets=project.img_classes,
                    classes=[],
            )
        if task_id == TaskType.IMAGE_EXTRACTION.name:
            obj = ImageExtractionTask(
                    type=TaskType.IMAGE_EXTRACTION.value,
                    results=[],
                    targets=project.img_entities,
                    entities=[],
            )

        push_new_task(pid, obj.dict())

    else:

        pull_task(pid, TaskType[task_id].value)



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


def delete_target(pid: str, task: str, name: str, describtion: str):
    conf = {
        TaskType.IMAGE_BOUNDINGBOX: "img_bounding_box_classes",
        TaskType.IMAGE_EXTRACTION: "img_entities",
        TaskType.IMAGE_CLASSIFICATION: "img_classes",
    }

    delete_class_project(
        pid,
        conf.get(TaskType[task]),
        Class(name=name, describtion=describtion).dict(),
    )

    delete_task_document(
        pid,
        TaskType[task].value,
        Class(name=name, describtion=describtion).dict()
    )


def get_exercises(pid: str) -> List[Excercies]:
    project = get_by_id(pid) 
    docs = find_all_imanges_by_project(pid)
    docs = map(lambda x: x.tasks, docs)
    docs = list(docs)
    docs = [item for sublist in docs for item in sublist]

    res = []

    for x in project.tasks:
        doc_tasks = filter(lambda y: y.type == x, docs)
        doc_tasks = list(doc_tasks)
        doc_done = list(filter(lambda y: len(y.results) >= 1,doc_tasks))
        res.append(
            Excercies(
                task_name=x, 
                data_type="Image", 
                processed=len(doc_done),
                total=len(doc_tasks)
            )
        )

    return res