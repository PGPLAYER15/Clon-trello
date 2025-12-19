from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.services.card_service import CardService
from app.domain.schemas.card import CardCreate, CardResponse, CardUpdate

router = APIRouter()


@router.post("/create", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(card_data: CardCreate, db: Session = Depends(get_db)):
    card_service = CardService(db)
    return card_service.create_card(
        title=card_data.title,
        list_id=card_data.list_id,
        description=card_data.description
    )


@router.get("/", response_model=list[CardResponse])
def get_cards_by_list(list_id: int, db: Session = Depends(get_db)):
    card_service = CardService(db)
    return card_service.get_cards_by_list(list_id)


@router.get("/{card_id}", response_model=CardResponse)
def get_card_by_id(card_id: int, db: Session = Depends(get_db)):
    card_service = CardService(db)
    card = card_service.get_card(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return card


@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card_data: CardUpdate, db: Session = Depends(get_db)):
    card_service = CardService(db)
    card = card_service.update_card(
        card_id=card_id,
        card_data=card_data
    )
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return card


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card_service = CardService(db)
    if not card_service.delete_card(card_id):
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return
