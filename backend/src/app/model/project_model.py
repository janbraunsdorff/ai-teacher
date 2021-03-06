from __future__ import annotations

from typing import Any, Dict, List
from unittest import result

from pydantic import BaseModel, Field

from app.model.document import Class, TaskType


class CreateProject(BaseModel):
    name: str


class ProjectHeader(BaseModel):
    id: str
    name: str
    created: str


class Project(BaseModel):
    id: str = Field(default="", alias="_id")
    name: str
    owner: str
    created: int
    tasks: List[TaskType]
    img_classes: List[Class]
    img_entities: List[Class]
    img_bounding_box_classes: List[Class]

    @classmethod
    def convert_from_mongo(cls, data) -> Project:
        data["_id"] = str(data["_id"])
        return Project(**data)

    class Config:
        use_enum_values = True


class Worker(BaseModel):
    id: str
    name: str
    alias: str
    is_worker: bool

    @classmethod
    def convert_from_mongo(cls, data):
        return Worker(
            id=str(data["_id"]),
            name=data["name"],
            alias=data["alias"],
            is_worker=False,
        )


class ToggleWorkerRequest(BaseModel):
    worker_id: str


class ImportRequest(BaseModel):
    path: str


class ImportResponse(BaseModel):
    num_imported: int
    error_files: List[str]


class TaskShort(BaseModel):
    name: str
    done: bool


class ImageMeta(BaseModel):
    org_name: str
    name: str
    shape: str
    tasks: List[TaskShort]
    results: Dict[str, Any]


class PossibleTask(BaseModel):
    name: str
    id: str
    type: str
    selected: bool


class ToggleTaskRequest(BaseModel):
    task_id: str


class ResultObjectRespnse(BaseModel):
    name: str
    id: str
    targets: List[Class]


class AddTargetRequest(BaseModel):
    task: str
    name: str
    describtion: str

class Excercies(BaseModel):
    task_name: str
    data_type: str
    processed: int
    total: int
