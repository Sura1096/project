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
) -> AccountResponse:
    return await account_service.register_account(account)


@company_router.post('/sign-up-complete')
async def register_company(
        company: CompanyRequest,
        account_service: Account = Depends(),
        company_service: Company = Depends(),
        user_service: User = Depends(),
        secret_service: Secret = Depends(),
        token: str = Depends(validate_auth_user),
) -> CompanyResponse:
    validate_email_from_token(token, company.email)
    return await company_service.register_company(company, account_service, user_service, secret_service)

