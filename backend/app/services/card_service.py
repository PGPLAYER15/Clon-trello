from typing import List as ListType
from app.infrastructure.repositories.card_repository import CardRepository
from app.domain.entities.card import Card
from app.domain.schemas.card import CardUpdate
from app.domain.Interfaces.tag_repository import ITagRepository

class CardService:
    def __init__(self,TagRepo:ITagRepository,cardRepo:CardRepository):
        self.tag_repo = TagRepo
        self.card_repo = cardRepo

    def get_cards_by_list(self, list_id: int) -> ListType[Card]:
        return self.card_repo.get_by_list(list_id)

    def get_card(self, card_id: int) -> Card | None:
        return self.card_repo.get_by_id(card_id)

    def create_card(self, title: str, list_id: int, description: str = None) -> Card:
        return self.card_repo.create_card(title, list_id, description)

    def update_card(self, card_id: int, card_data: CardUpdate) -> Card | None:
        return self.card_repo.update_card(card_id, card_data)

    def delete_card(self, card_id: int) -> bool:
        return self.card_repo.delete(card_id)

    def move_card(self, card_id: int, new_list_id: int) -> Card | None:
        return self.card_repo.move_card(card_id, new_list_id)

    def filter_by_tag(self, tag_name: str) -> ListType[Card]:
        return self.card_repo.filter_by_tag(tag_name)

    def add_tag(self,card_id: int,tag_id:int)-> bool:
        card = self.get_by_id(card_id)

        if not card:
            return False