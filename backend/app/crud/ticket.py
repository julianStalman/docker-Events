from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.user import User


from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
from app.enum.TicketStatus import TicketStatus
from app.schemas.ticket import TicketCreate, TicketBuy, TicketUpdateDetails


def create_ticket(*, db: Session, ticket: TicketCreate):

    db_ticket = Ticket(
        ticket_number = ticket.ticket_number, 
        price = ticket.price,
        status = ticket.status,
        event_id = ticket.event_id,
        user_id=ticket.user_id, 
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

def buy_ticket(*, db: Session, ticket_id: int, user_id: int):
    """
    Assign a user to a ticket and mark it as SOLD.
    """
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise ValueError(f"Ticket with ID {ticket_id} does not exist.")

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise ValueError(f"User with ID {user_id} does not exist.")

    if db_ticket.status == TicketStatus.SOLD:
        raise ValueError(f"Ticket with ID {ticket_id} is already sold.")

    if db_ticket.status == TicketStatus.CANCELLED:
        raise ValueError(f"Ticket with ID {ticket_id} is cancelled and cannot be purchased.")

    if db_ticket.status != TicketStatus.AVAILABLE:
        raise ValueError(f"Ticket with ID {ticket_id} is not available for purchase.")

    db_ticket.user_id = user_id
    db_ticket.status = TicketStatus.SOLD
    db_ticket.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_ticket)

    return db_ticket

def update_ticket_details(*, db: Session, ticket_id: int, ticket_update: TicketUpdateDetails):
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
