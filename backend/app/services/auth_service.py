from datetime import timedelta
from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.domain.entities.user import User


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def register(self, email: str, username: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        return self.user_repo.create_user(email, username, hashed_password)

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repo.get_by_email(email)

    def get_user_by_username(self, username: str) -> User | None:
        return self.user_repo.get_by_username(username)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)

    def create_token(self, user_id: int) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": str(user_id)},
            expires_delta=access_token_expires
        )
