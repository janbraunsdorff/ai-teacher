from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from app.model.document import TaskType


class CreateProject(BaseModel):
    name: str


class ProjectHeader(BaseModel):
    id: str
    name: str
    created: str


class Class(BaseModel):
    name: str
    describtion: str


class Project(BaseModel):
    id: str = Field(default="", alias="_id")
    name: str
    owner: str
    created: int
    tasks: List[TaskType]
    classes: List[Class]

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
