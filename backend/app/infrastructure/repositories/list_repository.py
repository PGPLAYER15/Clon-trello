from typing import List as ListType, Optional
from sqlalchemy.orm import Session, joinedload
from app.domain.entities.list import List
from app.domain.entities.card import Card
from .base import BaseRepository


class ListRepository(BaseRepository[List]):
    def __init__(self, db: Session):
        super().__init__(db, List)

    def get_by_id_with_cards(self, list_id: int) -> Optional[List]:
        return (
            self.db.query(List)
            .options(joinedload(List.cards))
            .filter(List.id == list_id)
            .first()
        )

    def get_by_board(self, board_id: int) -> ListType[List]:
        return (
            self.db.query(List)
            .options(joinedload(List.cards))
            .filter(List.board_id == board_id)
            .all()
        )

    def create_list(self, title: str, board_id: int) -> List:
        new_list = List(title=title, board_id=board_id)
        self.db.add(new_list)
        self.db.commit()
        self.db.refresh(new_list)
        return new_list

    def update_title(self, list_id: int, title: str) -> Optional[List]:
        db_list = self.get_by_id(list_id)
        if db_list:
            db_list.title = title
            self.db.commit()
            self.db.refresh(db_list)
        return db_list
