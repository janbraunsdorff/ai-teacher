import time
from typing import List

from mongomock import ObjectId
import pymongo

from app.database import collections
from app.model.document import Document, TaskType

db_name = "document"


def insert_document(document: Document):
    collections[db_name].insert_one(document.dict())


def find_all_imanges_by_project(pid: str) -> List[Document]:
    return [
        Document.convert_from_mongo(x)
        for x in collections[db_name].find({"project": pid})
    ]


def update_tasks(pid: str, tasks):
    collections[db_name].update_many(
        {"project": pid}, {"$set": {"tasks": tasks}}
    )


def push_new_task(pid, obj):
    collections[db_name].update_many(
        {"project": pid}, {"$push": {"tasks": obj}}
    )


def pull_task(pid, task_id):
    collections[db_name].update_many(
        filter={"project": pid},
        update={
            "$pull": {
                "tasks": {
                "type": task_id
                }
            }
        }
    )


def get_images_from_document(pid, iid) -> List[str]:
    return collections[db_name].find_one(
        {"project": pid, "_id": ObjectId(iid)}
    )["files"]


def push_class_document(pid, key, obj):
    collections[db_name].update_many(
        filter={
            "project": pid,
        },
        update={"$push": {"tasks.$[x].targets": obj}},
        array_filters=[{"x.type": {"$eq": key}}],
    )

def delete_task_document(pid, key, value):
    collections[db_name].update_many(
        filter={
            "project": pid,
        },
        update={"$pull": {"tasks.$[x].targets": value}},
        array_filters=[{"x.type": {"$eq": key}}],
    )

def get_latest_request(pid: str, type: TaskType):
    doc = collections[db_name].find(
        filter={
            "project": pid,
            "tasks": {
                "$elemMatch": {
                    "type": type.value,
                    "results.0": { # TODO for mulitble values
                        "$exists": False
                    }
                }
            }
        }
  
    ).sort("last_request", pymongo.ASCENDING)
    doc = list(doc)
    if len(doc) == 0:
        return None

    doc = doc[0]

    collections[db_name].update_one(
        filter={"_id": doc["_id"]},
        update={"$set": {"last_request": round(time.time() * 1000)}}
    )
    return Document.convert_from_mongo(doc)


def update_class(pid, did, data, task_type: TaskType):
    collections[db_name].update_one(
        filter={"project": pid, "_id": ObjectId(did)},
        update={"$push": {"tasks.$[x].results": data}},
        array_filters=[{"x.type": {"$eq": task_type.value}}]
    )

def remove_lables(pid: str, doc_id: str, type: str):
    collections[db_name].update_one(
        filter={"project": pid, "_id": ObjectId(doc_id)},
        update={"$set": {"tasks.$[x].results": []}},
        array_filters=[{"x.type": {"$eq": type}}]
    )