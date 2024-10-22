from fastapi import HTTPException, status

from src.schemas.task import CreateTask, TaskDB, TaskResponse, TaskResponseStatus
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class Task(BaseService):
    base_repository = 'task'

    @transaction_mode
    async def create_task(self, task: CreateTask) -> TaskResponse:
        await self.__check_if_author_exists(task.author_id)
        await self.__check_if_responsible_exists(task.responsible_id)
        await self.__check_if_watchers_exists(task.watchers)
        await self.__check_if_performers_exists(task.performers)

        result = await self.uow.task.create_task(**task.model_dump())
        return TaskResponse(
            status=status.HTTP_201_CREATED,
            data=result.to_pydantic_schema(),
        )

    @transaction_mode
    async def update_task(self, task: TaskDB) -> TaskResponse:
        await self.__check_if_author_exists(task.author_id)
        await self.__check_if_responsible_exists(task.responsible_id)
        await self.__check_if_watchers_exists(task.watchers)
        await self.__check_if_performers_exists(task.performers)

        await self.__check_if_task_exists(task.id)

        result = await self.uow.task.update_task(task)
        return TaskResponse(
            status=status.HTTP_200_OK,
            data=result.to_pydantic_schema(),
        )

    @transaction_mode
    async def delete_task(self, task_id: int) -> TaskResponseStatus:
        await self.__check_if_task_exists(task_id)

        await self.uow.task.delete_task(task_id)
        return TaskResponseStatus(
            status=status.HTTP_204_NO_CONTENT,
            detail='Task deleted.',
        )

    @transaction_mode
    async def __check_if_task_exists(self, task_id: int) -> None:
        task_in_db = await self.uow.task.get_task_by_id(task_id)
        if not task_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found.',
            )

    @transaction_mode
    async def __check_if_author_exists(self, author_id: int) -> None:
        author_in_db = await self.uow.employee.check_employee(author_id)
        if not author_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Author not found.',
            )

    @transaction_mode
    async def __check_if_responsible_exists(self, responsible_id: int) -> None:
        responsible_in_db = await self.uow.employee.check_employee(responsible_id)
        if not responsible_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Responsible not found.',
            )

    @transaction_mode
    async def __check_if_watchers_exists(self, watchers: list[int]) -> None:
        for watcher_id in watchers:
            watcher_in_db = await self.uow.employee.check_employee(watcher_id)
            if not watcher_in_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Watcher {watcher_id} not found.',
                )

    @transaction_mode
    async def __check_if_performers_exists(self, performers: list[int]) -> None:
        for performer_id in performers:
            performer_in_db = await self.uow.employee.check_employee(performer_id)
            if not performer_in_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Performer {performer_id} not found.',
                )
