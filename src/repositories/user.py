from sqlalchemy import select, update

from src.models.user import Secret, User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def check_user(self, email: str) -> User:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def change_email(self, old_email: str, new_email: str) -> None:
        query = (update(self.model)
                 .where(self.model.email == old_email)
                 .values(email=new_email)
                 .execution_options(synchronize_session='fetch'))
        await self.session.execute(query)

    async def change_name(
            self,
            email: str,
            new_first_name: str,
            new_last_name: str,
    ) -> None:
        query = (update(self.model)
                 .where(self.model.email == email)
                 .values(first_name=new_first_name, last_name=new_last_name)
                 .execution_options(synchronize_session='fetch'))
        await self.session.execute(query)


class SecretRepository(SqlAlchemyRepository):
    model = Secret

