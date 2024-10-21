from fastapi import HTTPException, status

from src.schemas.position import CreatePosition, PositionResponse, PositionStatus, UpdatePosition
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class Position(BaseService):
    base_repository = 'position'

    @transaction_mode
    async def create_position(self, position: CreatePosition) -> PositionResponse:
        await self.__check_if_structure_exists(position.structure_id)

        result = await self.uow.position.create_position(**position.model_dump())
        result = result.to_pydantic_schema()
        return PositionResponse(
            status=status.HTTP_201_CREATED,
            data=result,
        )

    @transaction_mode
    async def update_position(self, position: UpdatePosition) -> PositionResponse:
        await self.__check_if_position_exists(position.position_id)
        await self.__check_if_structure_exists(position.new_structure_id)

        result = await self.uow.position.update_position(**position.model_dump())
        result = result.to_pydantic_schema()
        return PositionResponse(
            status=status.HTTP_200_OK,
            data=result,
        )

    @transaction_mode
    async def delete_position(self, position_id: int) -> PositionStatus:
        await self.__check_if_position_exists(position_id)

        await self.uow.position.delete_position(position_id)
        return PositionStatus(
            status=status.HTTP_204_NO_CONTENT,
            detail='Position deleted.',
        )

    @transaction_mode
    async def __check_if_position_exists(self, position_id: int) -> None:
        position_in_db = await self.uow.position.get_position_by_id(position_id)
        if not position_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Position not found.',
            )

    @transaction_mode
    async def __check_if_structure_exists(self, structure_id: int) -> None:
        structure_in_db = await self.uow.structure.get_department_by_id(structure_id)
        if not structure_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Structure not found.',
            )
