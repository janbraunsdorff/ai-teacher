from typing import List, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    alias: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


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
