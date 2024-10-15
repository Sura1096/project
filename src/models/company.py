from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.schemas.company import AccountDB, CompanyDB


class Account(Base):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str]
    invite_token: Mapped[str]

    company = relationship('Company', back_populates='account')

    def to_pydantic_schema(self) -> AccountDB:
        return AccountDB(**self.__dict__)


class Company(Base):
    __tablename__ = 'company'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_id: Mapped[int] = mapped_column(ForeignKey('account.id'), nullable=True)
    company_name: Mapped[str]

    account = relationship('Account', back_populates='company')
    user = relationship('User', back_populates='company', cascade='all, delete-orphan')

    def to_pydantic_schema(self) -> CompanyDB:
        return CompanyDB(**self.__dict__)
