import datetime

from fastapi import HTTPException, status

import app.database.user as user_database
from app.database.project import all, get_by_id, insert_project
from app.model.project_model import Project, ProjectHeader, Worker
from app.model.user_models import User
from app.services import convert_timestamp


def get_project_header():
    return [
        ProjectHeader(
            id=project.id,
            name=project.name,
            created=convert_timestamp(project.created),
        )
        for project in all()
    ]


def create_project(project: Project, user: User):
    project = Project(
        name=project.name,
        owner=user.alias,
        created=datetime.datetime.utcnow().timestamp() * 1000,
        tasks=[],
        classes=[],
    )
    insert_project(project=project)


def get_worker(pid: str):
    return [
        Worker(
            id=str(x["_id"]),
            name=x["name"],
            is_worker=x["is_worker"],
            alias=x["alias"],
        )
        for x in user_database.get_worker_for_project(pid=pid)
    ]


def toggle_user(pid: str, wid: str, current_user: User):
    user_database.togel_project(wid, pid)


def check_for_project_owner(current_user: User, pid: str):
    project = get_by_id(pid)
    if project.owner != current_user.alias:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid permissions",
        )
