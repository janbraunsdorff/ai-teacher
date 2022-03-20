import datetime
from email.mime import image

import app.services.user_service as us
from app.database import collections
from app.model.project_model import Project
from app.model.user_models import User

time = int(datetime.datetime.utcnow().timestamp() * 1000)


def insert_user():
    user = {
        "alias": "alias",
        "password": us.get_password_hash("password"),
        "name": "username",
        "roles": ["worker"],
        "working_on": [],
    }

    collections["user"].insert_one(user)
    return user


def inser_project(
    user, tasks=[], img_classes=[], img_entities=[], img_bounding_box_classes=[]
):
    projects = [
        Project(
            name="p1",
            owner=user["alias"],
            created=time,
            tasks=tasks,
            img_classes=img_classes,
            img_entities=img_entities,
            img_bounding_box_classes=img_bounding_box_classes,
        ).dict()
    ]

    project_ids = collections["project"].insert_many(projects)

    for project, pid in zip(projects, project_ids.inserted_ids):
        project["id"] = str(pid)

    return projects
