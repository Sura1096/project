from pydantic import BaseModel, EmailStr, constr


class CreateUser(BaseModel):
    company_name: str
    first_name: str
    last_name: str
    email: EmailStr


class UserEmail(BaseModel):
    email: str
    username: str
    password: str


class RegisterUser(BaseModel):
    email: EmailStr
    token: str
    password: constr(min_length=8, max_length=16)


class UserSaveDb(BaseModel):
    company_id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserDB(BaseModel):
    id: int
    company_id: int
    first_name: str
    last_name: str
    email: str


class SecretSaveDb(BaseModel):
    user_id: int
    password: str


class SecretDB(BaseModel):
    id: int
    user_id: int
    password: str


class UpdateEmail(BaseModel):
    old_account: str
    new_account: str
    username: str
    password: str


class UpdateEmailDb(BaseModel):
    token: str
    old_account: str
    new_account: str


class UpdateName(BaseModel):
    account: str
    new_first_name: str
    new_last_name: str


class UserStatus(BaseModel):
    status: int


class UserResponse(BaseModel):
    status: int
    data: UserDB
