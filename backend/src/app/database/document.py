from typing import List

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
