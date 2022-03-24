from typing import List
from pydantic import BaseModel

class ClassificationTargets(BaseModel):
    name: str
    desc: str


class NextImage(BaseModel):
    id: str
    width: int
    height: int
    classes: List[ClassificationTargets]


class ClassificationResult(BaseModel):
    class_name: str
    document_id: str