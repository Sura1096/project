from src.schemas.company import CompanyRequest, RegisterAccount
from src.utils.security import hash_password
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class Account(BaseService):
    base_repository: str = 'account'

    @transaction_mode
    async def check_account(self, account: str):
        return await self.uow.account.check_account(account)

    @transaction_mode
    async def create_account(self, account: RegisterAccount):
        await self.uow.account.add_one(**account.model_dump())


class Company(BaseService):
    base_repository: str = 'company'

    @transaction_mode
    async def create_company(self, company: CompanyRequest):
        company.password = hash_password(company.password)
        await self.uow.company.add_one(**company.model_dump())
