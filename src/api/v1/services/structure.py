from fastapi import HTTPException, status

from src.schemas.structure import (
    CreateDepartmentRequest,
    DepartmentResponse,
    DepartmentStatus,
    UpdateDepartment,
)
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class Structure(BaseService):
    base_repository = 'structure'

    @transaction_mode
    async def create_department(
            self,
            department: CreateDepartmentRequest,
    ) -> DepartmentResponse:
        company = await self.uow.company.get_company_by_id(department.company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Company not found.',
            )
        result = await self.uow.structure.create_department(**department.model_dump())
        result = result.to_pydantic_schema()
        return DepartmentResponse(
            status=status.HTTP_201_CREATED,
            data=result,
        )

    @transaction_mode
    async def update_department(self, department: UpdateDepartment) -> DepartmentResponse:
        await self.__check_if_department(department.department_id)
        result = await self.uow.structure.update_department(**department.model_dump())
        result = result.to_pydantic_schema()
        return DepartmentResponse(
            status=status.HTTP_201_CREATED,
            data=result,
        )

    @transaction_mode
    async def delete_department(self, department_id: int) -> DepartmentStatus:
        await self.__check_if_department(department_id)
        await self.uow.structure.delete_department(department_id)
        return DepartmentStatus(
            status=status.HTTP_204_NO_CONTENT,
            detail='Department deleted.',
        )

    async def __check_if_department(self, department_id: int) -> None:
        department_id_in_db = await self.uow.structure.get_department_by_id(department_id)
        if not department_id_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Department not found.',
            )
