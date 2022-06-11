from tortoise.contrib.fastapi import register_tortoise
from data.model import *
from fastapi import FastAPI, Depends


TORTOISE_ORM = {
    "connections": {"default": 'sqlite://notesdb.sqlite'},
    "apps": {
        "models": {
            "models": ["data.model.user", "data.model.note", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url='sqlite://notesdb.sqlite',
        modules={"models": ["data.model.user", "data.model.note"]},
        generate_schemas=False,
        add_exception_handlers=False,
    )
