from fastapi import APIRouter, Depends

from src.api.v1.services.structure import Structure
from src.schemas.structure import CreateDepartmentRequest, DepartmentResponse, DepartmentStatus, UpdateDepartment
from src.utils.security import validate_auth_user

department_router = APIRouter(dependencies=[Depends(validate_auth_user)])


@department_router.post('/create-department')
async def create_department(
        department: CreateDepartmentRequest,
        structure_service: Structure = Depends(),
) -> DepartmentResponse:
    return await structure_service.create_department(department)


@department_router.patch('/update-department')
async def update_department(
        department: UpdateDepartment,
        structure_service: Structure = Depends(),
) -> DepartmentResponse:
    return await structure_service.update_department(department)


@department_router.delete('/delete-department')
async def delete_department(
        department_id: int,
        structure_service: Structure = Depends(),
) -> DepartmentStatus:
    return await structure_service.delete_department(department_id)
