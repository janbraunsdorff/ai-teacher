from enum import Enum
from html import entities
from typing import Dict, List, Union
from unittest import result

from pydantic import BaseModel, Field


##########################
## Result
##########################
class TaskResult(BaseModel):
    worker_id: str


class BoundingBox(BaseModel):
    x: int
    y: int
    w: int
    h: int


class ImageBoundingBoxResult(TaskResult):
    boxes: Dict[str, BoundingBox]


class ImageClassificationResult(TaskResult):
    clazz: str = Field(alias="class")


class ImageExtraction(TaskResult):
    data: Dict[str, Union[str, int]]


##########################
## Task
##########################
class TaskType(Enum):
    IMAGE_BOUNDINGBOX = "iamge_boundingbox"
    IMAGE_CLASSIFICATION = "image_classification"
    IMAGE_EXTRACTION = "image_extraction"


class Task(BaseModel):
    type: TaskType
    results: List[TaskResult]

    class Config:
        use_enum_values = True


class ImageBoundingBoxTask(Task):
    entities: List[str]


class ImageClassificationTask(Task):
    classes: List[str]


class ImageExtractionTask(Task):
    entities: List[str]


##########################
## Documenmt
##########################
class DocumentType(Enum):
    IMAGE = "image"
    AUDIO = "audio"
    TEXT = "text"
    STRUCT = "struct"


class Document(BaseModel):
    id: str = Field(default="", alias="_id")
    project: str
    type: DocumentType
    files: List[str]
    num_result: int
    tasks: List[
        Union[
            ImageBoundingBoxTask, ImageClassificationTask, ImageExtractionTask
        ]
    ]

    @classmethod
    def convert_from_mongo(cls, data):
        data["_id"] = str(data["_id"])
        return Document(**data)

    class Config:
        use_enum_values = True