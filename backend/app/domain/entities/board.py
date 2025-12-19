from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    color = Column(String(7), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="boards")

    lists = relationship(
        "List", 
        back_populates="board",
        cascade="all, delete-orphan",
        lazy="joined",
        order_by="List.id"
    )

    def __repr__(self):
        return f"<Board(id={self.id}, title='{self.title}')>"
