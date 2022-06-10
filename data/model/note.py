from data.model.base import MyBaseModel
from tortoise import fields


class Note(MyBaseModel):
    
    title = fields.CharField(max_length=30)
    body = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    user = fields.ForeignKeyField(model_name='models.User', related_name='notes')