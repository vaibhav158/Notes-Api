from tortoise.models import Model
from tortoise import fields


class User(Model):

    id: int = fields.IntField(pk=True)
    username = fields.CharField(max_length=30)
    password = fields.TextField()