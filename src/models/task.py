from datetime import date

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import ARRAY

from src.models.base import Base
from src.schemas.task import TaskDB, TaskStatus


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('employee.id'))
    responsible_id: Mapped[int] = mapped_column(ForeignKey('employee.id'))
    watchers: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    performers: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    deadline: Mapped[date]
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.OPEN)
    estimated_time_hours: Mapped[int]

    def to_pydantic_schema(self) -> TaskDB:
        return TaskDB(**self.__dict__)
