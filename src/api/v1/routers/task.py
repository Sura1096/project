from fastapi import APIRouter, Depends

from src.api.v1.services.task import Task
from src.schemas.task import CreateTask, TaskDB, TaskResponse, TaskResponseStatus
from src.utils.security import validate_auth_user

task_router = APIRouter(dependencies=[Depends(validate_auth_user)])


@task_router.post('/create-task')
async def create_task(
        task: CreateTask,
        task_service: Task = Depends(),
) -> TaskResponse:
    return await task_service.create_task(task)


@task_router.put('/update-task')
async def update_task(
        task: TaskDB,
        task_service: Task = Depends(),
) -> TaskResponse:
    return await task_service.update_task(task)


@task_router.delete('/delete-task')
async def delete_task(
        task_id: int,
        task_service: Task = Depends(),
) -> TaskResponseStatus:
    return await task_service.delete_task(task_id)
