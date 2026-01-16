from typing import List as ListType, Optional   
from app.domain.Interfaces.tag_repository import ITagRepository
from app.domain.entities.tag import Tag
from app.domain.schemas.tag import TagCreate, TagUpdate

class TagService:
    def __init__(self,tag_repo:ITagRepository):
        self.tag_repo = tag_repo
    
    def get_tags(self) -> ListType[Tag]:
        return self.tag_repo.get_all()
    
    def get_tag(self, tag_id: int) -> Optional[Tag]:
        return self.tag_repo.get_by_id(tag_id)
    
    def create_tag(self, tag_data: TagCreate) -> Tag:
        return self.tag_repo.create_tag(tag_data)
    
    def update_tag(self, tag_id: int, tag_data: TagUpdate) -> Optional[Tag]:
        return self.tag_repo.update_tag(tag_id, tag_data)
    
    def delete_tag(self, tag_id: int) -> bool:
        return self.tag_repo.delete_tag(tag_id)