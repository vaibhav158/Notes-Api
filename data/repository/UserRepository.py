from domain.model.user import User as DomainUser
from data.model.user import User as DBUser
from tortoise.contrib.pydantic import pydantic_model_creator


UserPydantic = pydantic_model_creator(
    DBUser, name='User', exclude_readonly=True)


class UserRepository():

    async def get_user_by_username(self, username: str) -> DomainUser:
        user_obj = await UserPydantic.from_queryset_single(DBUser.get(username=username))
        return DomainUser(
            username=user_obj.username,
            password=user_obj.password
        )

    async def add_user(self, user: DomainUser):
        await DBUser.create(username=user.username, password=user.password)
