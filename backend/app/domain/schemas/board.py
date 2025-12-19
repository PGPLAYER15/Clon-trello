from typing import List, Optional
from pydantic import BaseModel
from .list import ListResponse


class BoardBase(BaseModel):
    title: str
    description: Optional[str] = None
    color: str


class BoardCreate(BoardBase):
    pass


class BoardResponse(BoardBase):
    id: int
    lists: List[ListResponse] = []

    class Config:
        from_attributes = True
