from domain.model.user import User as DomainUser
from data.model.user import User as DBUser


class UserRepository():

    async def get_user_by_username(self, username: str) -> DomainUser:
        print(f'username: {username}')
        user = await DBUser.get(username=username)
        return DomainUser(
            id=user.id,
            username=user.username,
            password=user.password
        )

    async def add_user(self, username: str, hashed_password: str):
        await DBUser.create(username=username, password=hashed_password)
