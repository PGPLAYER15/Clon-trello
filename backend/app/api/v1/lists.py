from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.services.list_service import ListService
from app.services.card_service import CardService
from app.domain.schemas.list import ListCreate, ListResponse, ListUpdateCards

router = APIRouter()


@router.post("/", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
def create_list(list_data: ListCreate, db: Session = Depends(get_db)):
    list_service = ListService(db)
    return list_service.create_list(list_data.title, list_data.board_id)


@router.get("/", response_model=list[ListResponse])
def get_lists_by_board(board_id: int, db: Session = Depends(get_db)):
    list_service = ListService(db)
    return list_service.get_lists_by_board(board_id)


@router.get("/{list_id}", response_model=ListResponse)
def get_list_by_id(list_id: int, db: Session = Depends(get_db)):
    list_service = ListService(db)
    db_list = list_service.get_list(list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    return db_list


@router.put("/{list_id}", response_model=ListResponse)
def update_list(list_id: int, list_data: ListCreate, db: Session = Depends(get_db)):
    list_service = ListService(db)
    db_list = list_service.update_list(list_id, list_data.title)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    return db_list


@router.put("/{list_id}/cards", response_model=ListResponse)
def update_list_cards(list_id: int, cards_data: ListUpdateCards, db: Session = Depends(get_db)):
    list_service = ListService(db)
    card_service = CardService(db)
    
    db_list = list_service.get_list(list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    for card_id in cards_data.cards:
        card_service.move_card(card_id, list_id)
    
    return list_service.get_list(list_id)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    list_service = ListService(db)
    if not list_service.delete_list(list_id):
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    return
