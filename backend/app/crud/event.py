from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.schemas.ticket import TicketCreate 
from app.crud.ticket import create_ticket  


def create_event(*, db: Session, event: EventCreate, ticket_price: float):
    """
    Create a new event and generate tickets for it.

    Args:
        db (Session): Database session.
        event (EventCreate): Event creation schema.
        ticket_price (float): Price for each ticket.

    Returns:
        Event: The created event.
    """
    # Create the event
    db_event = Event(
        title=event.title,
        description=event.description,
        location=event.location,
        event_date=event.event_date,
        total_tickets=event.total_tickets,
        available_tickets=event.available_tickets,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Generate tickets with unique ticket numbers
    for ticket_number in range(1, event.total_tickets + 1):
        ticket_data = TicketCreate(
            ticket_number=f"{db_event.id}-{ticket_number}",  # Ensure uniqueness by including event_id
            price=ticket_price,
            status="available",
            event_id=db_event.id,
            user_id=None,
        )
        create_ticket(db=db, ticket=ticket_data)

    return db_event


def get_event_by_id(*, db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def get_all_events(*, db: Session):
    return db.query(Event).all()


def update_event(*, db: Session, event_id: int, event_update: EventUpdate):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None

    update_data = event_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db_event.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_event)

    return db_event


def delete_event(*, db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None

    db.delete(db_event)
    db.commit()

    return db_event
