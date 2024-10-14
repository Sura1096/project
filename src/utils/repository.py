from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_one_or_none(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_all(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs: Any) -> None:
        query = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def add_one_and_get_id(self, **kwargs: Any) -> int:
        query = insert(self.model).values(**kwargs).returning(self.model.id)
        obj_id = await self.session.execute(query)
        return obj_id.scalar_one()

    async def get_by_query_one_or_none(self, **kwargs: Any) -> Sequence[Base] | None:
        query = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def get_by_query_all(self, **kwargs: Any) -> Sequence[Base]:
        query = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res.scalars().all()
