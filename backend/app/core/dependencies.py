from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Config & DB
from app.infrastructure.database import get_db
from app.core.config import settings

# Repositories (Capa Infraestructura)
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.repositories.board_repository import BoardRepository
from app.infrastructure.repositories.list_repository import ListRepository
from app.infrastructure.repositories.card_repository import CardRepository
from app.infrastructure.repositories.tag_repository import TagRepository

# Services (Capa Aplicación)
from app.services.auth_service import AuthService
from app.services.board_service import BoardService
from app.services.list_service import ListService
from app.services.card_service import CardService
from app.services.tag_service import TagService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# --- Dependency para obtener el Usuario Actual (Auth) ---
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_repo = UserRepository(db)      
    auth_service = AuthService(user_repo)
    
    user = auth_service.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user


# --- Factories de Servicios (Para inyectar en tus Rutas) ---

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repo = UserRepository(db)
    return AuthService(user_repo)

def get_board_service(db: Session = Depends(get_db)) -> BoardService:
    board_repo = BoardRepository(db)
    return BoardService(board_repo)

def get_list_service(db: Session = Depends(get_db)) -> ListService:
    list_repo = ListRepository(db)
    return ListService(list_repo)

def get_tag_service(db: Session = Depends(get_db)) -> TagService:
    # Si decides usar Interface, aquí instanciarías TagRepository pero el tipo de retorno sería TagService
    tag_repo = TagRepository(db)
    return TagService(tag_repo)

def get_card_service(db: Session = Depends(get_db)) -> CardService:
    # CardService requiere DOS repositorios según tu código
    tag_repo = TagRepository(db)
    card_repo = CardRepository(db)
    return CardService(tag_repo, card_repo)