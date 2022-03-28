import io
from email.mime import image
from typing import List
from app.model.document import TaskType

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.model.user_models import User
from app.model.image_model import ClassificationResult, NextImage, ImageExtractionResult
from app.services.project_service import relabel
from app.services.image_service import extract, get_image_data, get_next_image, classifiy
from app.services.user_service import get_current_active_user, check_if_lable
from app.services.project_service import check_for_project_owner

image_router = APIRouter(prefix="/images", tags=["image"])

@image_router.get("/{pid}/next-class", response_model=NextImage)
def get_next_classification(
    pid, user: User = Depends(get_current_active_user)
):
    check_if_lable(user, pid)
    return get_next_image(pid, TaskType.IMAGE_CLASSIFICATION)


@image_router.post("/{pid}/classify")
def save_class(
    pid, 
    cmd: ClassificationResult, 
    user: User = Depends(get_current_active_user)
):
    check_if_lable(user, pid)
    classifiy(pid, cmd.document_id, user.alias, cmd.class_name, TaskType.IMAGE_CLASSIFICATION)


@image_router.get("/{pid}/relabel-classify/{doc_id}", response_model=NextImage)
def get_next_classification(
    pid,
    doc_id,
    user: User = Depends(get_current_active_user)
):
    check_for_project_owner(user, pid)
    return relabel(pid, doc_id, TaskType.IMAGE_CLASSIFICATION)


@image_router.get("/{pid}/next-extraction", response_model=NextImage)
def get_next_classification(
    pid, user: User = Depends(get_current_active_user)
):
    check_if_lable(user, pid)
    return get_next_image(pid, TaskType.IMAGE_EXTRACTION)


@image_router.post("/{pid}/extract")
def save_extraction(
    pid, 
    cmd: ImageExtractionResult, 
    user: User = Depends(get_current_active_user)
):
    check_if_lable(user, pid)
    extract(pid, user.alias, cmd.id, cmd.res, TaskType.IMAGE_EXTRACTION)


@image_router.get("/{pid}/relabel-extraction/{doc_id}", response_model=NextImage)
def get_next_classification(
    pid,
    doc_id,
    user: User = Depends(get_current_active_user)
):
    check_for_project_owner(user, pid)
    return relabel(pid, doc_id, TaskType.IMAGE_EXTRACTION)

@image_router.get("/{pid}/{image_id}")
def create_project(
    image_id, pid, user: User = Depends(get_current_active_user)
):
    data = get_image_data(pid, image_id)
    return StreamingResponse(io.BytesIO(data), media_type="image/png")
