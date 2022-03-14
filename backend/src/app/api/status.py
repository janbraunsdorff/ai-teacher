import time

from fastapi import APIRouter

from app.model.status_model import Status

status_router = APIRouter(prefix="/status")


@status_router.get("/", tags=["status"])
async def status() -> Status:
    return Status(status="OK", date=int(time.time() * 1000))
