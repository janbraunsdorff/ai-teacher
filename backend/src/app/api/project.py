from typing import Any

from fastapi import APIRouter, Depends

from app.model.user_models import User
from app.services.user_service import get_current_active_user

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.get("/all", response_model=Any)
def get_all(current_user: User = Depends(get_current_active_user)):
    print(current_user)
    return []
