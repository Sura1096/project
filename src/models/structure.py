from sqlalchemy import ForeignKey, Index, Integer, func
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship, remote
from sqlalchemy_utils import Ltree, LtreeType

from src.models.base import Base
from src.schemas.structure import DepartmentDB


class Structure(Base):
    __tablename__ = 'structure'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    path: Mapped[str] = mapped_column(LtreeType)
    company_id: Mapped[int] = mapped_column(ForeignKey('company.id'), nullable=True)

    company = relationship('Company', back_populates='structure')
    position = relationship('Position', back_populates='structure', cascade='all, delete-orphan')

    # Добавление relationship() для доступа к родительским или дочерним узлам узлов
    parent = relationship(
        'Structure',
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref='children',
    )

    # Установка индекса для поиска
    __table_args__ = (
        Index('ix_departments_path', path, postgresql_using='gist'),
    )

    def __init__(self, name: str, company_id: int) -> None:
        self.name = name
        self.company_id = company_id

    def set_id(self, new_id, parent=None) -> None:
        self.id = new_id
        ltree_id = Ltree(str(new_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    def to_pydantic_schema(self) -> DepartmentDB:
        dict_representation = self.__dict__.copy()
        dict_representation['path'] = str(self.path)
        return DepartmentDB(**dict_representation)
