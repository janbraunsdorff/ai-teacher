from typing import List

from bson.objectid import ObjectId

from app.database import collections
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
