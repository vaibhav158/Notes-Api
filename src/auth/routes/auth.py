from domain.model.user import User
from domain.model.jwt import Token
from data.repository.UserRepository import UserRepository
from fastapi import HTTPException, status, Depends
from src.auth.jwt_service import create_access_token_for_user
from src.auth.encryptor_service import get_password_hash
from src.config import AppSettings, get_app_settings
from typing import Dict


from fastapi import APIRouter


auth_router = APIRouter()


@auth_router.post("/register", response_model=User)
async def register_user(
    user_obj: User,
    app_settings: AppSettings = Depends(get_app_settings),
    user_repository: UserRepository = Depends()
):
    user = user_obj.dict()
    username = user["username"]
    password = user["password"]

    user_exists = True if await get_user_by_username(
        username=username) else False

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

    if not username or not password:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either Username or Passsword is not Valid"
        )

    if len(username) < 5:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is too short"
        )

    if len(password) < 8:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too short"
        )

    await user_repository.add_user(User(
        username=username,
        password=get_password_hash(password)
    ))

    return Token(
        access_token = get_access_token_for_user(user, app_settings)
    )


def get_access_token_for_user(user: Dict, settings: AppSettings) -> str:
    return create_access_token_for_user(user, str(settings.secret_key.get_secret_value())) 


async def get_user_by_username(username):

    try:
        return await UserRepository.get_user_by_username(username)
    except:
        return None
