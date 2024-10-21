from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.schemas.employee import EmployeeDB
from src.schemas.position import PositionDB


class Position(Base):
    __tablename__ = 'position'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    structure_id: Mapped[int] = mapped_column(ForeignKey('structure.id'), nullable=True)

    structure = relationship('Structure', back_populates='position')
    employee = relationship('Employee', back_populates='position', cascade='all, delete-orphan')

    def to_pydantic_schema(self) -> PositionDB:
        return PositionDB(**self.__dict__)


class Employee(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    position_id: Mapped[int] = mapped_column(ForeignKey('position.id'), nullable=True)

    user = relationship('User', back_populates='employee')
    position = relationship('Position', back_populates='employee')

    def to_pydantic_schema(self) -> EmployeeDB:
        return EmployeeDB(**self.__dict__)


