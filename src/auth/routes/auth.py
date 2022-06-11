from domain.model.user import User
from domain.model.jwt import Token
from data.repository.UserRepository import UserRepository
from fastapi import HTTPException, status, Depends
from src.auth.jwt_service import create_access_token_for_user
from src.auth.encryptor_service import get_password_hash
from src.config import AppSettings, get_app_settings
from typing import Dict
from src.dependencies.auth import get_current_user
from fastapi import APIRouter


auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post("/register", response_model=Token)
async def register_user(
    user: User,
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

    user_obj = User(
        username=user.username,
        password=get_password_hash(user.password)
    )

    print(user_obj.json())
    await user_repository.add_user(user_obj)

    return Token(
        access_token = get_access_token_for_user(user_obj, app_settings)
    )


def get_access_token_for_user(user: User, settings: AppSettings) -> str:
    return create_access_token_for_user(user, str(settings.secret_key.get_secret_value())) 


@auth_router.get('/user/me')
async def get_current_user_info(user: User = Depends(get_current_user)):
    return user