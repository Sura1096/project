from fastapi import HTTPException, status

from src.schemas.user import SecretSaveDb, UpdateName, UserDB, UserSaveDb
from src.utils.security import hash_password
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class User(BaseService):
    base_repository: str = 'users'

    @transaction_mode
    async def create_user(self, user: UserSaveDb) -> int:
        return await self.uow.user.add_one_and_get_id(**user.model_dump())

    @transaction_mode
    async def check_user(self, email: str) -> UserDB | None:
        result = await self.uow.user.check_user(email)
        if result:
            return result.to_pydantic_schema()
        return None

    @transaction_mode
    async def change_email(self, old_email: str, new_email: str) -> None:
        await self.uow.user.change_email(old_email, new_email)

    @transaction_mode
    async def change_name(self, name: UpdateName) -> None:
        await self.uow.user.change_name(name)


class Secret(BaseService):
    base_repository: str = 'secret'

    @transaction_mode
    async def add_secret(self, secret: SecretSaveDb) -> None:
        secret.password = hash_password(secret.password)
        await self.uow.secret.add_one(**secret.model_dump())


async def check_if_user_not_exists(account: str, user_service: User) -> UserDB:
    user_info = await user_service.check_user(account)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return user_info
