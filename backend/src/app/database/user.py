from app.database import user_collection
from app.model.user_models import MongoUser


def insert_user(user: MongoUser):
    user_collection.insert_one(user.dict())

def find_by_username(username: str):
    return user_collection.find_one({"username": username})
