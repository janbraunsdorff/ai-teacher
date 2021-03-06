from typing import List

from bson.objectid import ObjectId

from app.database import collections
from app.model.document import TaskType
from app.model.project_model import Project


def insert_project(project: Project):
    collections["project"].insert_one(project.dict())


def all() -> List[Project]:
    return [
        Project.convert_from_mongo(p) for p in collections["project"].find()
    ]


def get_by_id(pid) -> Project:
    return Project.convert_from_mongo(
        collections["project"].find_one({"_id": ObjectId(pid)})
    )


def toggle_active_tasks(pid: str, task_id: str) -> List[TaskType]:
    task = TaskType[task_id]
    tasks = collections["project"].find_one({"_id": ObjectId(pid)})["tasks"]
    if task.value in tasks:
        tasks.remove(task.value)
        to_add = False
    else:
        tasks.append(task.value)
        to_add = True

    collections["project"].update_one(
        {"_id": ObjectId(pid)}, {"$set": {"tasks": tasks}}
    )

    return tasks, to_add


def push_class_project(pid, key, obj):
    collections["project"].update_one(
        {"_id": ObjectId(pid)}, {"$push": {key: obj}}
    )

def delete_class_project(pid, key, obj):
    collections["project"].update_one(
        {"_id": ObjectId(pid)}, {"$pull": {key: obj}}
    )