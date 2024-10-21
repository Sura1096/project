from typing import Any

from sqlalchemy import delete, insert, select

from src.models.position import Employee
from src.utils.repository import SqlAlchemyRepository


class EmployeeRepository(SqlAlchemyRepository):
    model = Employee

    async def check_employee(self, employee_id: int) -> Employee | None:
        query = select(self.model).where(self.model.id == employee_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_employee(self, **kwargs: Any) -> Employee:
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete_employee(self, employee_id: int) -> None:
        query = delete(self.model).where(self.model.id == employee_id)
        await self.session.execute(query)
