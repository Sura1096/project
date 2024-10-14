from typing import Any

from src.utils.unit_of_work import UnitOfWork, transaction_mode


class BaseService:
    base_repository: str

    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    @transaction_mode
    async def add_one(self, **kwargs: Any) -> None:
        await self.uow.__dict__[self.base_repository].add_one(**kwargs)

    @transaction_mode
    async def add_one_and_get_id(self, **kwargs: Any) -> int:
        return await self.uow.__dict__[self.base_repository].add_one_and_get_id(**kwargs)

    @transaction_mode
    async def get_by_query_one_or_none(self, **kwargs: Any) -> Any:
        await self.uow.__dict__[self.base_repository].get_by_query_one_or_none(**kwargs)

    @transaction_mode
    async def get_by_query_all(self, **kwargs: Any) -> Any:
        await self.uow.__dict__[self.base_repository].get_by_query_all(**kwargs)
