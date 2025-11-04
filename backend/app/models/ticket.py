from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime
from enums.TicketStatus import TicketStatus

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.AVAILABLE, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_purchased = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    event = relationship("Event", back_populates="tickets")
    buyer = relationship("User", back_populates="tickets")