from sqlalchemy import select

from src.models.user import Secret, User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def check_user(self, email: str) -> User:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


class SecretRepository(SqlAlchemyRepository):
    model = Secret

