from typing import Any, Optional, Union

from pydantic import BaseModel, Field


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

    @classmethod
    def convert_from_mongo(cls, data):
        data["_id"] = str(data["_id"])
        return Project(**data)
