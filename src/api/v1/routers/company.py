from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.v1.services.company import Account, Company
from src.api.v1.services.user import Secret, User
from src.schemas.company import AccountResponse, AccountStatus, CompanyRequest, CompanyResponse, RegisterAccount
from src.schemas.user import UserEmail
from src.utils.security import validate_auth_user, validate_email_from_token

company_router = APIRouter()


@company_router.get('/check_account')
async def check_account(
        account: str,
        username: str,
        password: str,
        background_tasks: BackgroundTasks,
        account_service: Account = Depends(),
) -> AccountStatus:
    account = UserEmail(email=account, username=username, password=password)
    return await account_service.send_email(account, background_tasks)


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
        token: str = Depends(validate_auth_user),
) -> SuccessStatus:
    validate_email_from_token(token, company.email)
    account_in_db = await account_service.check_account(company.email)
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
