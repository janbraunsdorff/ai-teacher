import inspect
from typing import List

from mongomock import ObjectId

from app.database import collections
from app.model.document import Document

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
