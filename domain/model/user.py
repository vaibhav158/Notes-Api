from domain.model.base import MyBaseModel

class User(MyBaseModel):
    username: str
    password: str