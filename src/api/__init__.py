__all__ = [
    'router',
]
from fastapi import APIRouter

from src.api.v1.routers.company import company_router
from src.api.v1.routers.employee import employee_router
from src.api.v1.routers.position import position_router
from src.api.v1.routers.structure import department_router
from src.api.v1.routers.task import task_router
from src.api.v1.routers.user import user_router

router = APIRouter()
router.include_router(company_router, prefix='/v1/company', tags=['company'])
router.include_router(user_router, prefix='/v1/user', tags=['user'])
router.include_router(department_router, prefix='/v1/department', tags=['department'])
router.include_router(position_router, prefix='/v1/position', tags=['position'])
router.include_router(employee_router, prefix='/v1/employee', tags=['employee'])
router.include_router(task_router, prefix='/v1/task', tags=['task'])
