import pytest
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.crud.ticket import (
    create_ticket,
    get_ticket_by_id,
    get_tickets_by_event_id,
    get_tickets_by_user_id,
    update_ticket,
    delete_ticket,
)
from app.enum.TicketStatus import TicketStatus


def test_create_ticket(db, test_event):
    ticket_data = TicketCreate(
        ticket_number="TICKET123",
        price=50.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id, 
        user_id=None,
    )

    result = create_ticket(db=db, ticket=ticket_data)

    assert result.id is not None
    assert result.ticket_number == "TICKET123"
    assert result.price == 50.0
    assert result.status == TicketStatus.AVAILABLE  
    assert result.event_id == test_event.id  
    assert result.user_id is None