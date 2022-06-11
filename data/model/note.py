from tortoise.models import Model
from tortoise import fields


class Note(Model):
    
    id: int = fields.IntField(pk=True)
    title = fields.CharField(max_length=30)
    body = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    user = fields.ForeignKeyField(model_name='models.User', related_name='notes')