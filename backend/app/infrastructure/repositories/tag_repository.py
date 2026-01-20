from typing import List as ListType, Optional
from app.domain.Interfaces.tag_repository import ITagRepository
from datetime import datetime
from sqlalchemy.orm import Session
from app.domain.entities.tag import Tag
from app.domain.schemas.tag import TagCreate , TagUpdate , TagReponse
from .base import BaseRepository

class TagRepository(BaseRepository[Tag], ITagRepository):
    def __init__(self, db: Session):
        super().__init__(db, Tag)

    def get_by_id(self,tag_id:int) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.id == tag_id).first()
    
    def get_by_name(self, name: str) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.name == name).first()
    
    def get_all(self) -> ListType[Tag]:
        return self.db.query(Tag).all()
    
    def create_tag(self, tag_data: TagCreate) -> Tag:
        tag = Tag(name=tag_data.name, color=tag_data.color)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def update_tag(self, tag_id: int, tag_data: TagUpdate) -> Optional[Tag]:
        tag = self.get_by_id(tag_id)
        if tag:
            update_data = tag_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(tag, key, value)
            self.db.commit()
            self.db.refresh(tag)
        return tag
    
    def delete_tag(self, tag_id: int) -> bool:
        tag = self.get_by_id(tag_id)
        if tag:
            self.db.delete(tag)
            self.db.commit()
            return True
        return False
    
    def add_tag_to_card(self, tag_id: int, card_id: int) -> bool:
        tag = self.get_by_id(tag_id)
        if tag:
            tag.cards.append(card_id)
            self.db.commit()
            return True
        return False