from typing import List as ListType, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.domain.schemas.card import CardUpdate
from app.domain.entities.card import Card
from .base import BaseRepository


class CardRepository(BaseRepository[Card]):
    def __init__(self, db: Session):
        super().__init__(db, Card)

    def get_by_list(self, list_id: int) -> ListType[Card]:
        return self.db.query(Card).filter(Card.list_id == list_id).all()

    def create_card(self, title: str, list_id: int, description: str = None, due_date: datetime = None) -> Card:
        card = Card(title=title, list_id=list_id, description=description, due_date=due_date)
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def update_card(self, card_id: int, card_data: CardUpdate) -> Optional[Card]:
        card = self.get_by_id(card_id)
        if card:
            update_data = card_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(card, key, value)
            self.db.commit()
            self.db.refresh(card)
        return card

    def move_card(self, card_id: int, new_list_id: int) -> Optional[Card]:
        card = self.get_by_id(card_id)
        if card:
            card.list_id = new_list_id
            self.db.commit()
            self.db.refresh(card)
        return card
