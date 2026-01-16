from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user , get_board_service
from app.services.board_service import BoardService
from app.domain.schemas.board import BoardCreate, BoardResponse
from app.domain.entities.user import User

router = APIRouter()


@router.get("/", response_model=list[BoardResponse])
def read_boards(
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_user)
):
    return board_service.get_user_boards(current_user.id)


@router.get("/{board_id}", response_model=BoardResponse)
def read_board(
    board_id: int,
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_user)
):
    board = board_service.get_board(board_id)
    
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if not board_service.is_owner(board_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this board")
    
    return board


@router.post("/", response_model=BoardResponse)
def create_board(
    board: BoardCreate,
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_user)
):
    return board_service.create_board(board, current_user.id)


@router.delete("/{board_id}")
def delete_board(
    board_id: int,
    board_service: BoardService = Depends(get_board_service),
    current_user: User = Depends(get_current_user)
):
    board = board_service.get_board(board_id)
    
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if not board_service.is_owner(board_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this board")
    
    board_service.delete_board(board_id)
    return {"message": "Board deleted successfully"}
