from pydantic import BaseModel, EmailStr, constr


class CreateUser(BaseModel):
    company_name: str
    first_name: str
    last_name: str
    email: EmailStr


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
