from fastapi import BackgroundTasks, HTTPException, status

from src.schemas.company import AccountDB, CompanyDB, RegisterAccount
from src.schemas.user import (
    CreateUser,
    RegisterUser,
    SecretSaveDb,
    UpdateEmail,
    UpdateEmailDb,
    UpdateName,
    UserDB,
    UserEmail,
    UserResponse,
    UserSaveDb,
    UserStatus,
)
from src.utils.email_sender import send_token, send_token_to_user
from src.utils.security import hash_password
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class Secret(BaseService):
    base_repository: str = 'secret'

    @transaction_mode
    async def add_secret(self, secret: SecretSaveDb) -> None:
        secret.password = hash_password(secret.password)
        await self.uow.secret.add_one(**secret.model_dump())


class User(BaseService):
    base_repository: str = 'users'

    @transaction_mode
    async def create_user_db(self, user: UserSaveDb) -> int:
        return await self.uow.user.add_one_and_get_id(**user.model_dump())

    @transaction_mode
    async def check_user(self, email: str) -> UserDB | None:
        result = await self.uow.user.check_user(email)
        if result:
            return result.to_pydantic_schema()
        return None

    @transaction_mode
    async def change_email_in_db(self, old_email: str, new_email: str) -> None:
        await self.uow.user.change_email(old_email, new_email)

    @transaction_mode
    async def change_name_in_db(self, name: UpdateName) -> None:
        await self.uow.user.change_name(name)

    async def create_user(
            self,
            user: CreateUser,
            account_service,
            company_service,
    ) -> UserResponse:
        await self.__check_if_account_exists(user.email, account_service)
        company_info = await self.__check_if_company_exists(user.company_name, company_service)
        company_id = company_info.id
        user_info = UserSaveDb(
            company_id=company_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
        await self.create_user_db(user_info)
        return UserResponse(
            status=status.HTTP_201_CREATED,
            data=await self.check_user(user.email),
        )

    async def sign_up(
            self,
            email: UserEmail,
            background_tasks: BackgroundTasks,
            account_service,
    ) -> UserStatus:
        await self.__check_if_account_exists(email.email, account_service)
        background_tasks.add_task(send_token_to_user, email, background_tasks)
        return UserStatus(status=status.HTTP_200_OK)

    async def sign_up_complete(
            self,
            user: RegisterUser,
            account_service,
            secret_service: Secret,
    ) -> UserResponse:
        await self.__check_if_account_exists(user.email, account_service)
        await account_service.create_account(RegisterAccount(email=user.email, invite_token=user.token))
        user_info = await self.check_user(user.email)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found.',
            )
        await secret_service.add_secret(SecretSaveDb(user_id=user_info.id, password=user.password))
        return UserResponse(
            status=status.HTTP_201_CREATED,
            data=await self.check_user(user.email),
        )

    async def send_token_to_another_email(
            self,
            email: UpdateEmail,
            background_tasks: BackgroundTasks,
            account_service,
    ) -> UserStatus:
        old_account_in_db = await self.__check_if_account_not_exists(email.old_account, account_service)
        await self.__check_if_account_exists(email.new_account, account_service)
        background_tasks.add_task(send_token, old_account_in_db.invite_token, email, background_tasks)
        return UserStatus(status=status.HTTP_200_OK)

    async def change_email(
            self,
            email: UpdateEmailDb,
            account_service,
    ) -> UserResponse:
        old_account_in_db = await account_service.check_account(email.old_account)
        if not old_account_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Old Email not found.',
            )
        await account_service.change_email(email)
        await self.change_email_in_db(email.old_account, email.new_account)
        return UserResponse(
            status=status.HTTP_200_OK,
            data=await self.check_user(email.new_account),
        )

    async def change_name(
            self,
            name: UpdateName,
            account_service,
    ) -> UserResponse:
        account_in_db = await account_service.check_account(name.account)
        if not account_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found.',
            )
        await self.change_name_in_db(name)
        return UserResponse(
            status=status.HTTP_200_OK,
            data=await self.check_user(name.account),
        )

    @staticmethod
    async def __check_if_account_exists(account: str, account_service) -> None:
        account_in_db = await account_service.check_account(account)
        if account_in_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists.',
            )

    @staticmethod
    async def __check_if_company_exists(company_name: str, company_service) -> CompanyDB:
        company_info = await company_service.check_company(company_name)
        if not company_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Company not found.',
            )
        return company_info

    @staticmethod
    async def __check_if_account_not_exists(email: str, account_service) -> AccountDB:
        old_account_in_db = await account_service.check_account(email)
        if not old_account_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Old Email not found.',
            )
        return old_account_in_db
