from fastapi import APIRouter, Depends

from src.api.v1.services.employee import Employee
from src.schemas.employee import CreateEmployee, EmployeeResponse, EmployeeStatus
from src.utils.security import validate_auth_user

employee_router = APIRouter(dependencies=[Depends(validate_auth_user)])


@employee_router.post('/create-employee')
async def create_employee(
        employee: CreateEmployee,
        employee_service: Employee = Depends(),
) -> EmployeeResponse:
    return await employee_service.create_employee(employee)


@employee_router.delete('/delete-employee')
async def delete_employee(
        employee_id: int,
        employee_service: Employee = Depends(),
) -> EmployeeStatus:
    return await employee_service.delete_employee(employee_id)
