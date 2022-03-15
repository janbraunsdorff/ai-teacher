from typing import List, Optional

from pydantic import BaseModel


class Token(BaseModel):
    expired_in: str
    alias: str
    roles: List[str]

class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    alias: str
    name: str
    roles: List[str]


class UserInDB(User):
    hashed_password: str


class RegisterUserRequest(BaseModel):
    name: str
    alias: str
    password: str


class MongoUser(BaseModel):
    _id: str
    alias: str
    password: str
    name: str
    roles: List[str]
