from .auth import router as auth_router
from .boards import router as boards_router
from .lists import router as lists_router
from .cards import router as cards_router
from .tag import router as tag_router

__all__ = ["auth_router", "boards_router", "lists_router", "cards_router", "tag_router"]
