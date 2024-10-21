from typing import Any

from sqlalchemy import delete, insert, select, update

from src.models.position import Position
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = Position

    async def get_position_by_id(self, position_id: int) -> Position | None:
        query = select(self.model).where(self.model.id == position_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_position(self, **kwargs: Any) -> Position:
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def update_position(self, position_id: int, new_name: str, new_structure_id: int) -> Position | None:
        query = (
            update(self.model)
            .where(self.model.id == position_id)
            .values(name=new_name, structure_id=new_structure_id)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete_position(self, position_id: int) -> None:
        query = delete(self.model).where(self.model.id == position_id)
        await self.session.execute(query)
