from app.database import collections
from app.model.document import Document

db_name = "document"


def insert_document(document: Document):
    collections[db_name].insert_one(document.dict())
