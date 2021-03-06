import datetime
from datetime import timedelta
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.database.user import find_by_alias, insert_user
from app.model.user_models import MongoUser, TokenData, User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,  # type: ignore
        scopes: dict = None,  # type: ignore
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(
            flows=flows, scheme_name=scheme_name, auto_error=auto_error
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("token")
        if not authorization:
            authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param  # type: ignore


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(alias: str):
    user = find_by_alias(alias)
    return user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as err:
        raise credentials_exception
    user = get_user(alias=token_data.username)  # type: ignore
    if user is None:
        raise credentials_exception

    if not isinstance(user, User):
        user = User(**user)
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


def create_user(alias: str, password: str, name: str):
    user = MongoUser(
        alias=alias,
        name=name,
        password=get_password_hash(password),
        roles=["worker"],
        working_on=[],
    )
    if get_user(alias) is not None:
        raise HTTPException(status_code=409, detail="User already exists")

    insert_user(user)

def check_if_lable(user: User, pid: str):
    if pid not in user.working_on:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid permissions",
        )
        