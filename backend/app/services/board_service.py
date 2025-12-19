from typing import List
from sqlalchemy.orm import Session
from app.infrastructure.repositories.board_repository import BoardRepository
from app.domain.entities.board import Board
from app.domain.schemas.board import BoardCreate


class BoardService:
    def __init__(self, db: Session):
        self.board_repo = BoardRepository(db)

    def get_user_boards(self, user_id: int) -> List[Board]:
        return self.board_repo.get_by_user(user_id)

    def get_board(self, board_id: int) -> Board | None:
        return self.board_repo.get_by_id_with_lists(board_id)

    def create_board(self, board_data: BoardCreate, user_id: int) -> Board:
        return self.board_repo.create_board(
            title=board_data.title,
            description=board_data.description,
            color=board_data.color,
            user_id=user_id
        )

    def delete_board(self, board_id: int) -> bool:
        return self.board_repo.delete(board_id)

    def is_owner(self, board_id: int, user_id: int) -> bool:
        board = self.board_repo.get_by_id(board_id)
        return board is not None and board.user_id == user_id
