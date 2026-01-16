from typing import List as ListType
from sqlalchemy.orm import Session
from app.infrastructure.repositories.list_repository import ListRepository
from app.domain.entities.list import List


class ListService:
    def __init__(self,list_repo: ListRepository):
        self.list_repo = list_repo

    def get_lists_by_board(self, board_id: int) -> ListType[List]:
        return self.list_repo.get_by_board(board_id)

    def get_list(self, list_id: int) -> List | None:
        return self.list_repo.get_by_id_with_cards(list_id)

    def create_list(self, title: str, board_id: int) -> List:
        return self.list_repo.create_list(title, board_id)

    def update_list(self, list_id: int, title: str) -> List | None:
        return self.list_repo.update_title(list_id, title)

    def delete_list(self, list_id: int) -> bool:
        return self.list_repo.delete(list_id)
