from typing import Any

from fastapi import APIRouter, Depends

from app.model.project_model import CreateProject
from app.model.user_models import User
from app.services.project_service import create_project, get_project_header
from app.services.user_service import get_current_active_user

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/all", response_model=Any)
def get_all(current_user: User = Depends(get_current_active_user)):
    return get_project_header()


@project_router.post("/create")
def post_create_project(
    data: CreateProject, current_user: User = Depends(get_current_active_user)
):
    create_project(project=data, user=current_user)
