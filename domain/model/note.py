from domain.model.utils import *
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, BaseConfig


class Note(BaseModel):
    id: int
    title: str
    body: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None
    user_id: int

    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime: convert_datetime_to_realworld}
        alias_generator = convert_field_to_camel_case