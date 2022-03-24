import io
from email.mime import image
from typing import List
from app.model.document import TaskType

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.model.user_models import User
from app.model.image_model import ClassificationResult, NextImage
from app.services.image_service import get_image_data, get_next_image, classifiy
from app.services.user_service import get_current_active_user

image_router = APIRouter(prefix="/images", tags=["image"])

@image_router.get("/{pid}/next-class", response_model=NextImage)
def get_next_classification(
    pid, user: User = Depends(get_current_active_user)
):
    return get_next_image(pid, TaskType.IMAGE_CLASSIFICATION)


@image_router.post("/{pid}/classify")
def save_class(
    pid, 
    cmd: ClassificationResult, 
    user: User = Depends(get_current_active_user)
):
    classifiy(pid, cmd.document_id, user.alias, cmd.class_name, TaskType.IMAGE_CLASSIFICATION)



@image_router.get("/{pid}/{image_id}")
def create_project(
    image_id, pid, user: User = Depends(get_current_active_user)
):
    data = get_image_data(pid, image_id)
    return StreamingResponse(io.BytesIO(data), media_type="image/png")
