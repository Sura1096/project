from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.v1.services.company import (
    Account,
    Company,
    check_if_account_exists,
    check_if_account_not_exists,
    check_if_company_not_exists,
)
from src.api.v1.services.user import Secret, User, check_if_user_not_exists
from src.schemas.company import RegisterAccount
from src.schemas.user import CreateUser, RegisterUser, SecretSaveDb, UpdateEmail, UpdateEmailDb, UpdateName, UserSaveDb
from src.utils.email_sender import send_token, send_token_to_user
from src.utils.security import validate_auth_user

user_router = APIRouter(dependencies=[Depends(validate_auth_user)])


@user_router.post('/create_user')
async def create_user_in_db(
        user: CreateUser,
        account_service: Account = Depends(),
        user_service: User = Depends(),
        company_service: Company = Depends(),
) -> None:
    await check_if_account_exists(user.email, account_service)

    company_info = await check_if_company_not_exists(user.company_name, company_service)
    company_id = company_info.id
    user_info = UserSaveDb(
        company_id=company_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )
    await user_service.create_user(user_info)


@user_router.post('/sign-up')
async def sign_up_user(
        email: str,
        background_tasks: BackgroundTasks,
        account_service: Account = Depends(),
) -> None:
    await check_if_account_exists(email, account_service)
    background_tasks.add_task(send_token_to_user, email, background_tasks)


@user_router.post('/sign-up-complete')
async def sign_up_complete_user(
        user: RegisterUser,
        account_service: Account = Depends(),
        secret_service: Secret = Depends(),
        user_service: User = Depends(),
) -> None:
    await check_if_account_exists(user.email, account_service)
    await account_service.create_account(RegisterAccount(email=user.email, invite_token=user.token))
    user_info = await check_if_user_not_exists(user.email, user_service)
    await secret_service.add_secret(SecretSaveDb(user_id=user_info.id, password=user.password))


@user_router.post('/new-email')
async def send_token_to_another_email(
        email: UpdateEmail,
        background_tasks: BackgroundTasks,
        account_service: Account = Depends(),
) -> None:
    old_account_in_db = await check_if_account_not_exists(email.old_account, account_service)
    await check_if_account_exists(email.new_account, account_service)
    background_tasks.add_task(send_token, old_account_in_db.invite_token, email.new_account, background_tasks)


@user_router.patch('/change-email')
async def change_email_in_db(
        email: UpdateEmailDb,
        account_service: Account = Depends(),
        user_service: User = Depends(),
) -> None:
    old_account_in_db = await check_if_account_not_exists(email.old_account, account_service)
    await account_service.change_email(email)
    await user_service.change_email(email.old_account, email.new_account)


@user_router.patch('/change-name')
async def change_name(
        name: UpdateName,
        account_service: Account = Depends(),
        user_service: User = Depends(),
) -> None:
    old_account_in_db = await check_if_account_not_exists(name.account, account_service)
    await user_service.change_name(name)

