from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.v1.services.company import (
    Account,
    Company,
)
from src.api.v1.services.user import Secret, User
from src.schemas.user import (
    CreateUser,
    RegisterUser,
    UpdateEmail,
    UpdateEmailDb,
    UpdateName,
    UserEmail,
    UserResponse,
    UserStatus,
)
from src.utils.security import validate_auth_user

user_router = APIRouter(dependencies=[Depends(validate_auth_user)])


@user_router.post('/create_user')
async def create_user(
        user: CreateUser,
        account_service: Account = Depends(),
        user_service: User = Depends(),
        company_service: Company = Depends(),
) -> UserResponse:
    return await user_service.create_user(user, account_service, company_service)


@user_router.post('/sign-up')
async def sign_up(
        email: UserEmail,
        background_tasks: BackgroundTasks,
        account_service: Account = Depends(),
        user_service: User = Depends(),
) -> UserStatus:
    return await user_service.sign_up(email, background_tasks, account_service)


@user_router.post('/sign-up-complete')
async def sign_up_complete(
        user: RegisterUser,
        account_service: Account = Depends(),
        secret_service: Secret = Depends(),
        user_service: User = Depends(),
) -> UserResponse:
    return await user_service.sign_up_complete(user, account_service, secret_service)


@user_router.post('/new-email')
async def send_token_to_another_email(
        email: UpdateEmail,
        background_tasks: BackgroundTasks,
        account_service: Account = Depends(),
        user_service: User = Depends(),
) -> UserStatus:
    return await user_service.send_token_to_another_email(email, background_tasks, account_service)


@user_router.patch('/change-email')
async def change_email(
        email: UpdateEmailDb,
        account_service: Account = Depends(),
        user_service: User = Depends(),
) -> UserResponse:
    return await user_service.change_email(email, account_service)


@user_router.patch('/change-name')
async def change_name(
        name: UpdateName,
        account_service: Account = Depends(),
        user_service: User = Depends(),
) -> UserResponse:
    return await user_service.change_name(name, account_service)
