from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    list_id = Column(Integer, ForeignKey("lists.id"))
    check = Column(Boolean, nullable=False, default=False)
    due_date = Column(DateTime, nullable=True)

    list = relationship("List", back_populates="cards")
