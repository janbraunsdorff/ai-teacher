from typing import Any, List

from fastapi import APIRouter, Depends

import app.services.import_service as ims
import app.services.project_service as ps
from app.model.project_model import (
    AddTargetRequest,
    CreateProject,
    ImageMeta,
    ImportRequest,
    ImportResponse,
    PossibleTask,
    ResultObjectRespnse,
    ToggleTaskRequest,
    ToggleWorkerRequest,
    Worker,
)
from app.model.user_models import User
from app.services.user_service import get_current_active_user

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/all", response_model=Any)
def get_all(current_user: User = Depends(get_current_active_user)):
    return ps.get_project_header()


@project_router.post("/create")
def post_create_project(
    data: CreateProject, current_user: User = Depends(get_current_active_user)
):
    ps.create_project(project=data, user=current_user)


@project_router.get("/{pid}/worker", response_model=List[Worker])
def get_all_possible_workers(
    pid, current_user: User = Depends(get_current_active_user)
):

    return ps.get_worker(pid)


@project_router.post("/{pid}/toggle-worker")
def post_toggle_worker(
    pid,
    cmd: ToggleWorkerRequest,
    current_user: User = Depends(get_current_active_user),
):
    ps.check_for_project_owner(current_user, pid)
    return ps.toggle_user(pid, cmd.worker_id, current_user)


@project_router.post("/{pid}/import", response_model=ImportResponse)
def post_import(
    pid,
    cmd: ImportRequest,
    current_user: User = Depends(get_current_active_user),
):
    ps.check_for_project_owner(current_user, pid)
    imported, unknown_filetype = ims.import_and_convert_to_default(
        cmd.path, pid
    )

    return ImportResponse(num_imported=imported, error_files=unknown_filetype)


@project_router.get("/{pid}/images", response_model=List[ImageMeta])
def get_image_data(
    pid,
    user: User = Depends(get_current_active_user),
):
    return ps.get_images(pid)


@project_router.get("/{pid}/tasks", response_model=List[PossibleTask])
def get_tasks(
    pid,
    user: User = Depends(get_current_active_user),
):
    return ps.get_tasks(pid)


@project_router.post("/{pid}/toggle-task")
def post_toggle_tasks(
    pid,
    cmd: ToggleTaskRequest,
    user: User = Depends(get_current_active_user),
):
    return ps.toggle_task(pid, cmd.task_id)


@project_router.get(
    "/{pid}/reuslt-object", response_model=List[ResultObjectRespnse]
)
def get_result_objects(pid, user: User = Depends(get_current_active_user)):
    return ps.getResultObjects(pid)


@project_router.post(
    "/{pid}/add-target", response_model=List[ResultObjectRespnse]
)
def get_result_objects(
    pid, cmd: AddTargetRequest, user: User = Depends(get_current_active_user)
):
    return ps.add_target(pid, cmd.task, cmd.name, cmd.describtion)
