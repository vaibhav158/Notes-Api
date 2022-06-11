from domain.model.user import User
from domain.model.jwt import Token
from data.repository.user_repository import UserRepository
from fastapi import HTTPException, status, Depends
from src.auth.jwt_service import create_access_token_for_user
from src.auth.encryptor_service import get_password_hash, verify_password
from src.config import AppSettings, get_app_settings
from typing import Dict
from src.dependencies.auth import get_current_user
from fastapi import APIRouter
from pydantic import BaseModel


auth_router = APIRouter(prefix='/auth', tags=['auth'])


class UserResponse(BaseModel):
    id: int
    username: str
    token: Token


class UserRequest(BaseModel):
    username: str
    password: str


@auth_router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserRequest,
    app_settings: AppSettings = Depends(get_app_settings),
    user_repository: UserRepository = Depends()
):

    try:
        user_obj = await user_repository.get_user_by_username(username=user.username)
    except:
        user_obj = None

    if user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

    if not user.username or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either Username or Passsword is not Valid"
        )

    if len(user.username) < 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is too short"
        )

    if len(user.password) < 8:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too short"
        )

    await user_repository.add_user(user.username, get_password_hash(user.password))

    user_obj = await user_repository.get_user_by_username(username=user.username)

    token = Token(
        access_token=get_access_token_for_user(user_obj.username, app_settings)
    )

    return UserResponse(
        id=user_obj.id,
        username=user_obj.username,
        token = token
    )


def get_access_token_for_user(username, settings: AppSettings) -> str:
    return create_access_token_for_user(username, str(settings.secret_key.get_secret_value()))


@auth_router.get('/user/me')
async def get_current_user_info(user: User = Depends(get_current_user)):
    return user


@auth_router.post('/login', response_model=UserResponse)
async def login_user(
    user: UserRequest,
    app_settings: AppSettings = Depends(get_app_settings),
    user_repository: UserRepository = Depends()
):
    try:
        user_obj = await user_repository.get_user_by_username(username=user.username)
    except:
        user_obj = None

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username doesn't exists"
        )

    if not user.username or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either Username or Passsword is not Valid"
        )

    is_password_valid = verify_password(
        plain_password=user.password, hashed_password=user_obj.password)

    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password"
        )

    token = Token(
        access_token=get_access_token_for_user(user_obj.username, app_settings)
    )

    return UserResponse(
        id=user_obj.id,
        username=user_obj.username,
        token = token
    )
