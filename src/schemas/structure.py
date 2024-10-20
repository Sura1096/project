from pydantic import BaseModel


class CreateDepartmentRequest(BaseModel):
    name: str
    parent_id: int
    company_id: int


class DepartmentDB(BaseModel):
    id: int
    name: str
    path: str
    company_id: int


class UpdateDepartment(BaseModel):
    department_id: int
    new_name: str


class DepartmentResponse(BaseModel):
    status: int
    data: DepartmentDB


class ChildDepartmentsResponse(BaseModel):
    status: int
    data: list[DepartmentDB]


class DepartmentStatus(BaseModel):
    status: int
    detail: str
