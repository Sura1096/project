from sqlalchemy import Sequence, delete, select, update

from src.models.structure import Structure
from src.utils.repository import SqlAlchemyRepository

id_seq = Sequence('structure_id_seq')


class StructureRepository(SqlAlchemyRepository):
    model = Structure

    async def create_department(self, name: str, parent_id: int, company_id: int) -> Structure | None:
        parent_id_in_db = await self.get_department_by_id(parent_id)
        new_department = self.model(name=name, company_id=company_id)
        new_id = await self.session.execute(id_seq)
        new_department.set_id(new_id, parent_id_in_db)

        self.session.add(new_department)
        return await self.get_department_by_id(new_department.id)

    async def get_department_by_id(self, department_id: int) -> Structure | None:
        query = select(self.model).where(self.model.id == department_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_department(self, department_id: int, new_name: str) -> Structure | None:
        query = update(self.model).where(self.model.id == department_id).values(name=new_name).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete_department(self, department_id: int) -> None:
        department_to_delete = await self.get_department_by_id(department_id)
        query = delete(self.model).where(self.model.path.descendant_of(department_to_delete.path))
        await self.session.execute(query)
