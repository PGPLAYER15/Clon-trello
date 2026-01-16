from fastapi import APIRouter,Depends,HTTPException,status
from app.core.dependencies import get_tag_service
from app.domain.schemas.tag import TagCreate,TagUpdate,TagReponse
from app.services.tag_service import TagService

router = APIRouter()

@router.get("/tags", response_model=list[TagReponse])
def get_tags(tag_service: TagService = Depends(get_tag_service)):
    return tag_service.get_tags()

@router.get("/tags/{tag_id}", response_model=TagReponse)
def get_tag(tag_id: int, tag_service: TagService = Depends(get_tag_service)):
    tag = tag_service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag

@router.post("/tags", response_model=TagReponse)
def create_tag(tag_data: TagCreate, tag_service: TagService = Depends(get_tag_service)):
    return tag_service.create_tag(tag_data)

@router.put("/tags/{tag_id}", response_model=TagReponse)
def update_tag(tag_id: int, tag_data: TagUpdate, tag_service: TagService = Depends(get_tag_service)):
    tag = tag_service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag_service.update_tag(tag_id, tag_data)

@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, tag_service: TagService = Depends(get_tag_service)):
    if not tag_service.delete_tag(tag_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return
