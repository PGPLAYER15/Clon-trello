from typing import List as ListType
from sqlalchemy.orm import Session
from app.infrastructure.repositories.card_repository import CardRepository
from app.domain.entities.card import Card
from datetime import datetime
from app.domain.schemas.card import CardUpdate

class CardService:
    def __init__(self, db: Session):
        self.card_repo = CardRepository(db)

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