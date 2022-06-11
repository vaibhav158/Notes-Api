from datetime import datetime, timedelta
from typing import Dict

from jose import jwt
from pydantic import ValidationError
from fastapi import HTTPException, status
from jose import JWTError

from domain.model.user import User
from domain.model.jwt import JWTPayload, JWTPrincipal


JWT_SUBJECT = "username"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # One Week


def create_jwt_token(
    jwt_content: dict,
    secret_key: str,
    expires_delta: timedelta,
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(JWTPayload(exp=expire, sub=JWT_SUBJECT).dict())
    print(to_encode)
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token_for_user(user: User, secret_key: str) -> str:
    return create_jwt_token(
        jwt_content=JWTPrincipal(username=user.username).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def get_username_from_token(token: str, secret_key: str) -> str:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload["username"]

    except JWTError:
        raise credentials_exception
