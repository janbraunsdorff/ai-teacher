import io
from email.mime import image

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.model.user_models import User
from app.services.image_service import get_image_data
from app.services.user_service import get_current_active_user

image_router = APIRouter(prefix="/images", tags=["image"])


@image_router.get("/{pid}/{image_id}")
def create_project(
    image_id, pid, user: User = Depends(get_current_active_user)
):
    data = get_image_data(pid, image_id)
    return StreamingResponse(io.BytesIO(data), media_type="image/png")
