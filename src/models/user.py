from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.schemas.user import SecretDB, UserDB


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('company.id'), nullable=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]

    company = relationship('Company', back_populates='user')
    secret = relationship('Secret', back_populates='user', cascade='all, delete-orphan')
    employee = relationship('Employee', back_populates='user', cascade='all, delete-orphan')

    def to_pydantic_schema(self) -> UserDB:
        return UserDB(**self.__dict__)


class Secret(Base):
    __tablename__ = 'secret'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    password: Mapped[str]

    user = relationship('User', back_populates='secret')

    def to_pydantic_schema(self) -> SecretDB:
        return SecretDB(**self.__dict__)
