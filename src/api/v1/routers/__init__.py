__all__ = [
    'company_router',
    'department_router',
    'employee_router',
    'position_router',
    'user_router',
]

from src.api.v1.routers.company import company_router
from src.api.v1.routers.employee import employee_router
from src.api.v1.routers.position import position_router
from src.api.v1.routers.structure import department_router
from src.api.v1.routers.user import user_router
