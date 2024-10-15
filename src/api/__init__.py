__all__ = [
    'router',
]
from fastapi import APIRouter

from src.api.v1.routers.company import company_router
from src.api.v1.routers.user import user_router

router = APIRouter()
router.include_router(company_router, prefix='/v1/company', tags=['company'])
router.include_router(user_router, prefix='/v1/user', tags=['user'])
