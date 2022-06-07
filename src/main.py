from fastapi import FastAPI, Depends, Header, HTTPException, status
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
import uvicorn
from loguru import logger
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime, timedelta

from starlette.middleware.cors import CORSMiddleware

import logging
from src.logging import InterceptHandler

from src.config import get_app_settings


def get_application():

    settings = get_app_settings()
    settings.configure_logging()


    app = FastAPI(**settings.fastapi_kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_application()


@app.get("/")
async def index_route():
    return {
        "message": "Hello, World!"
    }


# SECRET_KEY = "d04b9d7a34f0ccf23b5e0c511383e6ff645bb4632a1a1ff7440f2d386f3f21cf"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7    # 1 Week


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str


# class RequestUser(BaseModel):
#     username: str
#     passwd: str


# class User(Model):
#     id = fields.IntField(pk=True)
#     username = fields.CharField(max_length=30, unique=True)
#     passwd = fields.TextField()

#     notes: fields.ReverseRelation["Note"]


# class Note(Model):
#     id = fields.IntField(pk=True)
#     title = fields.CharField(max_length=50)
#     body = fields.TextField()
#     created_at = fields.DatetimeField(auto_now_add=True)
#     modified_at = fields.DatetimeField(auto_now=True)

#     user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
#         "models.User", related_name="notes"
#     )


# UserPydantic = pydantic_model_creator(User, name="User")
# UserInPydantic = pydantic_model_creator(
#     User, name="UserIn", exclude_readonly=True)
# NotePydantic = pydantic_model_creator(Note, name="Note")
# NoteInPydantic = pydantic_model_creator(
#     Note, name="NoteIn", exclude_readonly=True)


# async def get_current_user(token: str) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     scheme, _, param = token.partition(" ")
#     print(scheme)

#     if not token or scheme.lower() != "bearer":
#         raise credentials_exception

#     try:
#         payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception

#     user = await get_current_user(username)

#     if not user:
#         raise credentials_exception

#     return user


# async def get_user_by_username(username):
#     return await User.get(username=username)


# def create_access_token(payload: dict, expires_delta: timedelta | None = None):
#     to_encode = payload.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# @app.on_event(event_type="shutdown")
# async def app_shutdown_actions():
#     logger.info(
#         "app stopped, bye.",
#     )


# @app.get("/")
# async def index():
#     return {"message": "Hello World"}


# @app.post("/auth/register", response_model=Token)
# async def register_user(user: UserInPydantic):
#     print(user.username)
#     is_valid_credentials = check_valid_credentials(
#         user.username, user.passwd
#     )
#     if not is_valid_credentials:
#         raise HTTPException(
#             status.HTTP_400_BAD_REQUEST,
#             detail="Username or Password is not Valid"
#         )
#     hashed_passwd = pwd_context.hash(user.passwd)
#     is_username_available = await check_is_username_available(username=user.username)

#     print(is_username_available)

#     if not is_username_available:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username is already in use."
#         )

#     user_obj = User(username=user.username, passwd=hashed_passwd)
#     await user_obj.save()

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         payload={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# async def check_is_username_available(username):
#     return await User.exists(username=username)


# # Checks whether the username and password is not none or empty
# # and has required char counts
# def check_valid_credentials(username, passwd):
#     if not username or passwd:
#         return False
#     elif username.count < 5 or passwd.count < 8:
#         return False
#     return True


# @app.post("/auth/login", response_model=Token)
# async def login_user(user: UserInPydantic):
#     user_obj = await get_user_by_username(user.username)

#     if not user_obj:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No User with this Username exists."
#         )
#     is_passwd_valid = validate_password(
#         provided_passwd=user.passwd,
#         hashed_passwd=user_obj.passwd
#     )

#     if not is_passwd_valid:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect Password"
#         )

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         payload={"sub": user_obj.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/all_notes", response_model=List[NotePydantic])
# async def get_all_notes(user: UserInPydantic = Depends(get_current_user)):
#     return await NotePydantic.from_queryset(Note.get_or_none(user.id))


# @app.post("/note/create")
# async def create_new_note(note: NoteInPydantic, user: UserInPydantic = Depends(get_current_user)):
#     note_obj = Note(title=note.title, body=note.body, user_id=user.id)
#     await note_obj.save()


# def validate_password(provided_passwd, hashed_passwd):
#     return pwd_context.verify(provided_passwd, hashed_passwd)


# @app.get("/user/me", response_model=UserPydantic)
# def get_current_user_info(token=Header()):
#     user_obj = get_current_user(token)

#     return {

#         "username": user_obj.username,
#         "passwd": user_obj.passwd
#     }


# register_tortoise(
#     app=app,
#     db_url='sqlite://notesdb.sqlite',
#     modules={'models': ['main']},
#     generate_schemas=True,
#     add_exception_handlers=True
# )
