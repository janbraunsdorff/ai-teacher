from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.project import project_router
from app.api.status import status_router
from app.api.user import user_router

api = FastAPI()

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api.include_router(status_router)
api.include_router(user_router)
api.include_router(project_router)
