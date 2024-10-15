from sqlalchemy import select

from src.models.company import Account, Company
from src.utils.repository import SqlAlchemyRepository


class AccountRepository(SqlAlchemyRepository):
    model = Account

    async def check_account(
            self,
            account: str,
    ) -> Account | None:
        query = select(self.model).where(self.model.email == account)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


class CompanyRepository(SqlAlchemyRepository):
    model = Company

    async def check_company(self, company_name: str) -> Company | None:
        query = select(self.model).where(self.model.company_name == company_name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
