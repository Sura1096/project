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


async def check_if_account_exists(account: str, account_service: Account) -> None:
    account_in_db = await account_service.check_account(account)
    if account_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )


async def check_if_account_not_exists(account: str, account_service: Account) -> AccountDB:
    account_in_db = await account_service.check_account(account)
    if not account_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return account_in_db


async def check_if_company_not_exists(company_name: str, company_service: Company) -> CompanyDB:
    company_info = await company_service.check_company(company_name)
    if not company_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return company_info
