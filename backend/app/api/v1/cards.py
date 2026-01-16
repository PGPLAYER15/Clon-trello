from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_card_service
from app.services.card_service import CardService
from app.domain.schemas.card import CardCreate, CardResponse, CardUpdate

router = APIRouter()


@router.post("/create", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(card_data: CardCreate,card_service: CardService = Depends(get_card_service)):
    return card_service.create_card(
        title=card_data.title,
        list_id=card_data.list_id,
        description=card_data.description
    )


@router.get("/", response_model=list[CardResponse])
def get_cards_by_list(list_id: int, card_service: CardService = Depends(get_card_service)):
    return card_service.get_cards_by_list(list_id)


@router.get("/filter_by_tag", response_model=list[CardResponse])
def filter_by_tag(tag_name: str, card_service: CardService = Depends(get_card_service)):
    return card_service.filter_by_tag(tag_name)



@router.get("/{card_id}", response_model=CardResponse)
def get_card_by_id(card_id: int, card_service: CardService = Depends(get_card_service)):
    card = card_service.get_card(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return card


@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card_data: CardUpdate, card_service: CardService = Depends(get_card_service)):
    card = card_service.update_card(
        card_id=card_id,
        card_data=card_data
    )
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return card


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, card_service: CardService = Depends(get_card_service)):
    if not card_service.delete_card(card_id):
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return
