from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.domain.schemas.card import CardCreate, CardResponse, CardUpdate
from app.services.card_service import CardService
from app.core.dependencies import get_card_service
from app.core.exceptions import DatabaseError, NotFoundError, ValidationError
from datetime import datetime
from typing import Optional

router = APIRouter()


@router.post("/create", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(card_data: CardCreate, card_service: CardService = Depends(get_card_service)):
    try:
        return card_service.create_card(
            title=card_data.title,
            list_id=card_data.list_id,
            description=card_data.description
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la tarjeta: {str(e)}"
        )


@router.get("/", response_model=list[CardResponse])
def get_cards_by_list(list_id: int, card_service: CardService = Depends(get_card_service)):
    try:
        return card_service.get_cards_by_list(list_id)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener las tarjetas: {str(e)}"
        )


@router.get("/filter_by_tag", response_model=list[CardResponse])
def filter_by_tag(tag_name: str, card_service: CardService = Depends(get_card_service)):
    try:
        if not tag_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de la etiqueta no puede estar vacío"
            )
        return card_service.filter_by_tag(tag_name)
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al filtrar tarjetas: {str(e)}"
        )


@router.get("/search", response_model=list[CardResponse])
def search_cards(
    q: Optional[str] = Query(None, description="Buscar tarjeta por nombre"),
    tag_id: Optional[list[int]] = Query(None, description="IDs de etiquetas"),
    due_before: Optional[datetime] = Query(None, description="Vencimiento antes de"),
    due_after: Optional[datetime] = Query(None, description="Vencimiento después de"),
    card_service: CardService = Depends(get_card_service)
):
    try:
        # Validar que due_before sea posterior a due_after
        if due_before and due_after and due_before < due_after:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha 'due_before' debe ser posterior a 'due_after'"
            )
        return card_service.search_cards(q=q, tags_ids=tag_id, due_before=due_before, due_after=due_after)
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al buscar tarjetas: {str(e)}"
        )


@router.get("/{card_id}", response_model=CardResponse)
def get_card_by_id(card_id: int, card_service: CardService = Depends(get_card_service)):
    try:
        card = card_service.get_card(card_id)
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarjeta no encontrada"
            )
        return card
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener la tarjeta: {str(e)}"
        )


@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card_data: CardUpdate, card_service: CardService = Depends(get_card_service)):
    try:
        card = card_service.update_card(
            card_id=card_id,
            card_data=card_data
        )
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarjeta no encontrada"
            )
        return card
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar la tarjeta: {str(e)}"
        )


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, card_service: CardService = Depends(get_card_service)):
    try:
        if not card_service.delete_card(card_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarjeta no encontrada"
            )
        return
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar la tarjeta: {str(e)}"
        )

