from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=False)
    event_date = Column(DateTime, nullable=False)
    total_tickets = Column(Integer, nullable=False)
    available_tickets = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    tickets = relationship("Ticket", back_populates="event", lazy="select", cascade="all, delete-orphan")

