from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    board_id = Column(Integer, ForeignKey("boards.id"))

    board = relationship("Board", back_populates="lists")
    cards = relationship(
        "Card", 
        back_populates="list",
        cascade="all, delete-orphan",
        lazy="joined"
    )
