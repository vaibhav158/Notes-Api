# noqa:WPS201
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import get_app_settings, AppSettings
from domain.model.user import User
from src.utils import error_messages
from src.auth import jwt_service as jwt
from data.repository.user_repository import UserRepository
from src.utils import error_messages

HEADER_KEY = "Authorization"


class MyAPIKeyHeader(APIKeyHeader):
    async def __call__(  # noqa: WPS610
        self,
        request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=error_messages.AUTHENTICATION_REQUIRED,
            )


def _get_authorization_header(
    api_key: str = Security(MyAPIKeyHeader(name=HEADER_KEY)),
    settings: AppSettings = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
        print(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_messages.WRONG_TOKEN_PREFIX,
        )
    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_messages.WRONG_TOKEN_PREFIX,
        )

    return token


async def get_current_user(
    users_repo: UserRepository = Depends(),
    token: str = Depends(_get_authorization_header),
    settings: AppSettings = Depends(get_app_settings),
) -> User:
    try:
        username = jwt.get_username_from_token(
            token,
            str(settings.secret_key.get_secret_value()),
        )
        print(f"username {username}")
        return await users_repo.get_user_by_username(username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_messages.MALFORMED_PAYLOAD,
        )
