import enum
from datetime import date

from pydantic import BaseModel


class TaskStatus(enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In progress'
    CLOSED = 'Closed'


class TaskDB(BaseModel):
    id: int
    title: str
    description: str
    author_id: int
    responsible_id: int
    watchers: list[int]
    performers: list[int]
    deadline: date
    status: TaskStatus
    estimated_time_hours: int


class CreateTask(BaseModel):
    title: str
    description: str
    author_id: int
    responsible_id: int
    watchers: list[int]
    performers: list[int]
    deadline: date
    status: TaskStatus
    estimated_time_hours: int


class TaskResponse(BaseModel):
    status: int
    data: TaskDB


class TaskResponseStatus(BaseModel):
    status: int
    detail: str
