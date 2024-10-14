from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Account(Base):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str]
    invite_token: Mapped[str]


class Company(Base):
    __tablename__ = 'company'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    company_name: Mapped[str]
