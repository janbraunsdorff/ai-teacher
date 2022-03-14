from fastapi import FastAPI

from app.api.status import status_router
from fastapi.middleware.cors import CORSMiddleware

from app.api.user import user_router

api = FastAPI()

origins = ['*']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



api.include_router(status_router)
api.include_router(user_router)
