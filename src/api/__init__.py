__all__ = [
    'router',
]
from fastapi import APIRouter

from src.api.v1.routers.company import company_router

router = APIRouter()
router.include_router(company_router, prefix='/v1', tags=['company'])
