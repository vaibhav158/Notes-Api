from tortoise.models import Model
from tortoise import fields


class MyBaseModel(Model):
    id: int = fields.IntField(pk=True)

    class Meta:
        abstract = True