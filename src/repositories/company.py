from sqlalchemy import select, update

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

    async def change_email(
            self,
            old_email: str,
            new_email: str,
            new_token: str,
    ) -> None:
        query = (update(self.model)
                 .where(self.model.email == old_email)
                 .values(email=new_email, invite_token=new_token)
                 .execution_options(synchronize_session='fetch'))
        await self.session.execute(query)


class CompanyRepository(SqlAlchemyRepository):
    model = Company

    async def check_company(self, company_name: str) -> Company | None:
        query = select(self.model).where(self.model.company_name == company_name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
