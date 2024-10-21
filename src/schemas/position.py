from pydantic import BaseModel


class PositionDB(BaseModel):
    id: int
    name: str
    structure_id: int


class CreatePosition(BaseModel):
    name: str
    structure_id: int


class UpdatePosition(BaseModel):
    position_id: int
    new_name: str
    new_structure_id: int


class PositionResponse(BaseModel):
    status: int
    data: PositionDB


class PositionStatus(BaseModel):
    status: int
    detail: str
