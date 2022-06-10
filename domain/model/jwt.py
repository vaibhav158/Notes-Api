from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class JWTPayload(BaseModel):
    exp: datetime
    sub: str


class JWTPrincipal(BaseModel):
    username: str
