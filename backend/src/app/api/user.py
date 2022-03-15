from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.model.user_models import RegisterUserRequest, Token, User
from app.services.user_service import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_user,
    get_current_active_user,
)

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/register", response_model=Token)
async def register(user: RegisterUserRequest, response: Response):
    create_user(user.alias, user.password, user.name)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.alias}, expires_delta=access_token_expires
    )
    response.set_cookie("token", access_token, httponly=True, secure=False)

    return {
        "expired_in": datetime.utcnow().timestamp() * 1000.0,
        "alias": user.alias,
        "roles": ["worker"]
    }


@user_router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["alias"]}, expires_delta=access_token_expires
    )
    
    response.set_cookie("token", access_token, httponly=True, secure=False)

    return {
        "expired_in": datetime.utcnow().timestamp() * 1000.0,
        "alias": user["alias"],
        "roles": user["roles"]
    }


@user_router.get("/self", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
