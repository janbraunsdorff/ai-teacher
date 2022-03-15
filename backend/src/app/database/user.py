from app.database import collections
from app.model.user_models import MongoUser


def insert_user(user: MongoUser):
    collections["user"].insert_one(user.dict())


def find_by_username(username: str):
    return collections["user"].find_one({"username": username})
