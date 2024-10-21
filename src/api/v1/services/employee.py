from fastapi import HTTPException, status

from src.schemas.employee import CreateEmployee, EmployeeResponse, EmployeeStatus
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class Employee(BaseService):
    base_repository = 'employee'

    @transaction_mode
    async def create_employee(self, employee: CreateEmployee) -> EmployeeResponse:
        result = await self.uow.employee.create_employee(**employee.model_dump())
        result = result.to_pydantic_schema()
        return EmployeeResponse(
            status=status.HTTP_201_CREATED,
            data=result,
        )

    @transaction_mode
    async def delete_employee(self, employee_id: int) -> EmployeeStatus:
        employee_id_in_db = await self.uow.employee.check_employee(employee_id)
        if not employee_id_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Employee not found.',
            )
        await self.uow.employee.delete_employee(employee_id)
        return EmployeeStatus(
            status=status.HTTP_204_NO_CONTENT,
            detail='Employee deleted.',
        )
