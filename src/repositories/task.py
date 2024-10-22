from typing import Any

from sqlalchemy import delete, insert, select, update

from src.models.task import Task
from src.schemas.task import TaskDB
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = Task

    async def get_task_by_id(self, task_id: int) -> Task | None:
        query = select(self.model).where(self.model.id == task_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_task(self, **kwargs: Any) -> Task:
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def update_task(self, task: TaskDB) -> Task:
        query = update(self.model).where(self.model.id == task.id).values(**task.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete_task(self, task_id: int) -> None:
        query = delete(self.model).where(self.model.id == task_id)
        await self.session.execute(query)
