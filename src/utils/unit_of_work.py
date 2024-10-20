import functools
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any

from src.db.database import async_session_maker
from src.repositories.company import AccountRepository, CompanyRepository
from src.repositories.employee import EmployeeRepository
from src.repositories.position import PositionRepository
from src.repositories.structure import StructureRepository
from src.repositories.user import SecretRepository, UserRepository


class AbstractUnitOfWork(ABC):
    account: AccountRepository
    company: CompanyRepository
    user: UserRepository
    secret: SecretRepository
    structure: StructureRepository
    position: PositionRepository
    employee: EmployeeRepository

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.account = AccountRepository(self.session)
        self.company = CompanyRepository(self.session)
        self.user = UserRepository(self.session)
        self.secret = SecretRepository(self.session)
        self.structure = StructureRepository(self.session)
        self.position = PositionRepository(self.session)
        self.employee = EmployeeRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


def transaction_mode(func):
    @functools.wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
