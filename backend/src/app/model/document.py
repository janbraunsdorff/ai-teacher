from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Union, Optional

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
    clazz: str


class ImageExtraction(TaskResult):
    data: Dict[str, Union[str, int]]


##########################
## Task
##########################
class TaskType(Enum):
    IMAGE_BOUNDINGBOX = "Image Bounding Box"
    IMAGE_CLASSIFICATION = "Image Classification"
    IMAGE_EXTRACTION = "Image Extraction"


class Class(BaseModel):
    name: str
    describtion: str


class Task(BaseModel):
    type: TaskType
    targets: List[Class]
    results: List[Union[ImageBoundingBoxResult, ImageClassificationResult, ImageExtraction]]

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
    original_name: str
    type: DocumentType
    files: List[str]
    num_result: int
    last_request: int
    tasks: List[
        Union[
            ImageBoundingBoxTask, ImageClassificationTask, ImageExtractionTask
        ]
    ]

    @classmethod
    def convert_from_mongo(cls, data) -> Document:
        data["_id"] = str(data["_id"])
        return Document(**data)

    class Config:
        use_enum_values = True
