from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
from app.enum.TicketStatus import TicketStatus
from app.schemas.ticket import TicketCreate, TicketUpdate


def create_ticket(*, db: Session, ticket: TicketCreate):

    db_ticket = Ticket(
        ticket_number = ticket.ticket_number, 
        price = ticket.price,
        status = ticket.status,
       
       
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    return db_ticket

def get_ticket_by_id(*, db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def get_tickets_by_event_id(*, db: Session, event_id: int):
    return db.query(Ticket).filter(Ticket.event_id == event_id).all()


def get_tickets_by_user_id(*, db: Session, user_id: int):
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()


def update_ticket(*, db: Session, ticket_id: int, ticket_update: TicketUpdate):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        return None

    update_data = ticket_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)

    db_ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_ticket)

    return db_ticket


def delete_ticket(*, db: Session, ticket_id: int):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        return None

    db.delete(db_ticket)
    db.commit()

    return db_ticket