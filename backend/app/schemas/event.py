from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    event_date: datetime
    total_tickets: int
    available_tickets: int


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    event_date: Optional[datetime] = None
    total_tickets: Optional[int] = None
    available_tickets: Optional[int] = None


class EventInDBBase(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Event(EventInDBBase):
    pass
