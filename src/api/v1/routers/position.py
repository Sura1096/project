from fastapi import APIRouter, Depends

from src.api.v1.services.position import Position
from src.schemas.position import CreatePosition, PositionResponse, PositionStatus, UpdatePosition
from src.utils.security import validate_auth_user

position_router = APIRouter(dependencies=[Depends(validate_auth_user)])


@position_router.post('/create-position')
async def create_position(
        position: CreatePosition,
        position_service: Position = Depends(),
) -> PositionResponse:
    return await position_service.create_position(position)


@position_router.put('/update-position')
async def update_position(
        position: UpdatePosition,
        position_service: Position = Depends(),
) -> PositionResponse:
    return await position_service.update_position(position)


@position_router.delete('/delete-position')
async def delete_position(
        position_id: int,
        position_service: Position = Depends(),
) -> PositionStatus:
    return await position_service.delete_position(position_id)

