from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.domain.entities.board import Board
from app.domain.entities.list import List as ListEntity
from .base import BaseRepository


class BoardRepository(BaseRepository[Board]):
    def __init__(self, db: Session):
        super().__init__(db, Board)

    def get_by_id_with_lists(self, board_id: int) -> Optional[Board]:
        return (
            self.db.query(Board)
            .options(
                joinedload(Board.lists)
                .joinedload(ListEntity.cards)
            )
            .filter(Board.id == board_id)
            .first()
        )

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Board]:
        return (
            self.db.query(Board)
            .filter(Board.user_id == user_id)
            .options(
                joinedload(Board.lists)
                .joinedload(ListEntity.cards)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_board(self, title: str, description: str, color: str, user_id: int) -> Board:
        board = Board(
            title=title,
            description=description,
            color=color,
            user_id=user_id
        )
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board
