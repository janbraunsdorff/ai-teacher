from bson.objectid import ObjectId

from app.database import collections
from app.model.user_models import MongoUser


def insert_user(user: MongoUser):
    collections["user"].insert_one(user.dict())


def find_by_alias(username: str):
    return collections["user"].find_one({"alias": username})


def get_all():
    return collections["user"].find({})


def get_worker_for_project(pid, all=True):
    worker = list(collections["user"].find({"working_on": {"$in": [pid]}}))
    for w in worker:
        w["is_worker"] = True

    other = list(collections["user"].find({"working_on": {"$nin": [pid]}}))
    for o in other:
        o["is_worker"] = False

    return list(worker) + list(other)


def togel_project(wid: str, pid: str):
    projects = collections["user"].find_one({"_id": ObjectId(wid)})[
        "working_on"
    ]
    if pid in projects:
        projects.remove(pid)
    else:
        projects.append(pid)

    collections["user"].update_one(
        {"_id": ObjectId(wid)}, {"$set": {"working_on": projects}}
    )
