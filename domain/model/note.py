from domain.model.base import MyBaseModel
from datetime import datetime
from typing import Optional


class Note(MyBaseModel):
    title: str
    body: str
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = None
    user_id: int