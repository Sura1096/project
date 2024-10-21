from pydantic import BaseModel, ConfigDict, EmailStr, constr

from src.schemas.user import UserEmail


class RegisterAccount(BaseModel):
    email: str
    invite_token: str


class MailBody(BaseModel):
    to: UserEmail
    subject: str
    body: str


class AccountDB(BaseModel):
    id: int
    email: str
    invite_token: str


class AccountStatus(BaseModel):
    status: int
    detail: str


class AccountResponse(BaseModel):
    status: int
    data: AccountDB


class CompanyRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    first_name: str
    last_name: str
    company_name: str


class CompanySaveDb(BaseModel):
    email_id: int
    company_name: str


class CompanyDB(BaseModel):
    id: int
    email_id: int
    company_name: str


class CompanyResponse(BaseModel):
    status: int
    data: CompanyDB
