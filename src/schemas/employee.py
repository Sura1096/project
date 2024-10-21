from pydantic import BaseModel


class EmployeeDB(BaseModel):
    id: int
    user_id: int
    position_id: int


class CreateEmployee(BaseModel):
    user_id: int
    position_id: int


class EmployeeResponse(BaseModel):
    status: int
    data: EmployeeDB


class EmployeeStatus(BaseModel):
    status: int
    detail: str
