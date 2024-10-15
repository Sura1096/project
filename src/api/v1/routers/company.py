from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.v1.services.company import Account, Company, check_if_account_exists, check_if_account_not_exists
from src.api.v1.services.user import Secret, User
from src.schemas.company import CompanyRequest, CompanySaveDb, RegisterAccount, SuccessStatus
from src.schemas.user import SecretSaveDb, UserSaveDb
from src.utils.email_sender import send_token_to_admin

company_router = APIRouter()


@company_router.get('/check_account')
async def check_account(
        account: str,
        background_tasks: BackgroundTasks,
        account_service: Account = Depends(),
) -> SuccessStatus:
    await check_if_account_exists(account, account_service)
    background_tasks.add_task(send_token_to_admin, account, background_tasks)
    return SuccessStatus(status='Success')


@company_router.post('/sign-up')
async def register_account(
        account: RegisterAccount,
        account_service: Account = Depends(),
) -> SuccessStatus:
    await check_if_account_exists(account.email, account_service)
    await account_service.create_account(account)
    return SuccessStatus(status='Success')


@company_router.post('/sign-up-complete')
async def register_company(
        company: CompanyRequest,
        account_service: Account = Depends(),
        company_service: Company = Depends(),
        user_service: User = Depends(),
        secret_service: Secret = Depends(),
) -> SuccessStatus:
    account_in_db = await check_if_account_not_exists(company.email, account_service)
    data = CompanySaveDb(email_id=account_in_db.id, company_name=company.company_name)
    company_id = await company_service.create_company_and_get_id(data)

    user = UserSaveDb(
        company_id=company_id,
        first_name=company.first_name,
        last_name=company.last_name,
        email=company.email,
    )
    user_id = await user_service.create_user(user)
    await secret_service.add_secret(SecretSaveDb(user_id=user_id, password=company.password))
    return SuccessStatus(status='Success')
