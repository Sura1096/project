__all__ = [
    'company_router',
    'department_router',
    'user_router',
]

from src.api.v1.routers.company import company_router
from src.api.v1.routers.structure import department_router
from src.api.v1.routers.user import user_router
