import datetime

from app.database.project import all, insert_project
from app.model.project_model import Project, ProjectHeader
from app.model.user_models import User
from app.services import convert_timestamp


def get_project_header():
    print(all())
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
    )
    insert_project(project=project)
