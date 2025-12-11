from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import board as board_model
from app.schemas import board as board_schema
from app.models.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[board_schema.BoardResponse])
def read_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return board_model.get_boards_by_user(db, current_user.id)

@router.get("/{board_id}", response_model=board_schema.BoardResponse)
def read_board(
    board_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    board = board_model.get_board(db, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this board")
    return board

@router.post("/", response_model=board_schema.BoardResponse)
def create_board(
    board: board_schema.BoardCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return board_model.create_board(db, board, current_user.id)

@router.delete("/{board_id}")
def delete_board(
    board_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    board = board_model.get_board(db, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this board")
    board_model.delete_board(db, board_id)
    return {"message": "Board deleted successfully"}