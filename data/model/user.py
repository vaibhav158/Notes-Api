from data.model.base import MyBaseModel
from tortoise import fields


class User(MyBaseModel):
    username = fields.CharField(max_length=30)
    password = fields.TextField()