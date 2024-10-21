from fastapi import BackgroundTasks, HTTPException, status

from src.api.v1.services.user import Secret, User
from src.schemas.company import (
    AccountDB,
    AccountResponse,
    AccountStatus,
    CompanyDB,
    CompanyRequest,
    CompanyResponse,
    CompanySaveDb,
    RegisterAccount,
)
from src.schemas.user import SecretSaveDb, UpdateEmailDb, UserEmail, UserSaveDb
from src.utils.email_sender import send_token_to_admin
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class Account(BaseService):
    base_repository: str = 'account'

    @transaction_mode
    async def check_account(self, account: str) -> AccountDB | None:
        result = await self.uow.account.check_account(account)
        if result:
            return result.to_pydantic_schema()
        return None

    @transaction_mode
    async def create_account(self, account: RegisterAccount) -> None:
        await self.uow.account.add_one(**account.model_dump())

    @transaction_mode
    async def change_email(self, email: UpdateEmailDb) -> None:
        await self.uow.account.change_email(email)

    async def send_email(self, account: UserEmail, background_tasks: BackgroundTasks) -> AccountStatus:
        await self.__check_if_account_exists(account.email)
        background_tasks.add_task(send_token_to_admin, account, background_tasks)
        return AccountStatus(status=status.HTTP_200_OK, detail='An invite token has been sent to your email address.')

    async def register_account(self, account: RegisterAccount) -> AccountResponse:
        await self.__check_if_account_exists(account.email)
        await self.create_account(account)
        return AccountResponse(
            status=status.HTTP_201_CREATED,
            data=await self.check_account(account.email),
        )

    async def __check_if_account_exists(self, account: str) -> None:
        account_in_db = await self.check_account(account)
        if account_in_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists.',
            )


class Company(BaseService):
    base_repository: str = 'company'

    @transaction_mode
    async def create_company(self, company: CompanyRequest) -> None:
        await self.uow.company.add_one(**company.model_dump())

    @transaction_mode
    async def create_company_and_get_id(self, company: CompanySaveDb) -> int:
        return await self.uow.company.add_one_and_get_id(**company.model_dump())

    @transaction_mode
    async def check_company(self, company_name: str) -> CompanyDB | None:
        result = await self.uow.company.check_company(company_name)
        if result:
            return result.to_pydantic_schema()
        return None

    async def register_company(
            self,
            company: CompanyRequest,
            account_service: Account,
            user_service: User,
            secret_service: Secret,
    ) -> CompanyResponse:
        account_in_db = await self.__check_if_account_exists(company.email, account_service)
        data = CompanySaveDb(email_id=account_in_db.id, company_name=company.company_name)
        company_id = await self.create_company_and_get_id(data)

        user = UserSaveDb(
            company_id=company_id,
            first_name=company.first_name,
            last_name=company.last_name,
            email=company.email,
        )
        user_id = await user_service.create_user_db(user)
        await secret_service.add_secret(SecretSaveDb(user_id=user_id, password=company.password))
        return CompanyResponse(
            status=status.HTTP_201_CREATED,
            data=await self.check_company(company.company_name),
        )

    @staticmethod
    async def __check_if_account_exists(account: str, account_service: Account) -> AccountDB:
        account_in_db = await account_service.check_account(account)
        if not account_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Email not found.',
            )
        return account_in_db

