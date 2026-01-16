from pydantic import BaseModel
from typing import Optional

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    color: str

class TagUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    
class TagReponse(TagBase):
    id: int
    name: str
    color: str
    
    class Config:
        from_attributes = True