from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.enum.TicketStatus import TicketStatus

class TicketBase(BaseModel):
    ticket_number: str
    price: float
    status: TicketStatus = TicketStatus.AVAILABLE


class TicketCreate(TicketBase):
    event_id: int
    user_id: Optional[int] = None


class TicketUpdate(BaseModel):
    price: Optional[float] = None
    status: Optional[TicketStatus] = None


class TicketInDBBase(TicketBase):
    id: int
    user_id: Optional[int] = None
    event_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Ticket(TicketInDBBase):
    pass