from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, EmailStr, constr


class RegisterAccount(BaseModel):
    email: str
    invite_token: str


class MailBody(BaseModel):
    to: str
    subject: str
    body: str


class AccountDB(BaseModel):
    id: int
    email: str
    invite_token: str


class CompanyRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    first_name: str
    last_name: str
    company_name: str


@dataclass
class AdminJwtPayload:
    sub: str
    email: str


@dataclass
class SuccessStatus:
    status: str
