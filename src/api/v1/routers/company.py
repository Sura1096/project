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
    account_in_db = await account_service.check_account(account)
    if not account_in_db:
        payload = AdminJwtPayload(sub='admin', email=account)
        token = encode_jwt(payload)
        data = {
            'to': account,
            'subject': 'Token',
            'body': token,
        }
        background_tasks.add_task(send_email, MailBody(**data))
        return SuccessStatus(status='Success')
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Email {account} is already in use by someone.',
    )


@company_router.post('/sign-up')
async def register_account(
        account: RegisterAccount,
        account_service: Account = Depends(),
) -> SuccessStatus:
    account_in_db = await account_service.check_account(account.email)
    if not account_in_db:
        await account_service.create_account(account)
        return SuccessStatus(status='Success')
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Email {account} is already in use by someone.',
    )


@company_router.post('/sign-up-complete')
async def register_company(
        company: CompanyRequest,
        account_service: Account = Depends(),
        company_service: Company = Depends(),
) -> SuccessStatus:
    account_in_db = await account_service.check_account(company.email)
    if account_in_db:
        await company_service.create_company(company)
        return SuccessStatus(status='Success')
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Email {company.email} is already in use by someone.',
    )
