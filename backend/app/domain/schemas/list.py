from pydantic import BaseModel
from typing import List, Optional
from .card import CardResponse


class ListBase(BaseModel):
    title: str


class ListCreate(ListBase):
    board_id: int


class ListUpdate(BaseModel):
    title: Optional[str] = None


class ListUpdateCards(BaseModel):
    cards: List[int]


class ListResponse(BaseModel):
    id: int
    title: str
    board_id: int
    cards: Optional[List[CardResponse]] = []

    class Config:
        from_attributes = True
