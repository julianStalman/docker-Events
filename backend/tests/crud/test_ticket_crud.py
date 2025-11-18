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


def test_get_ticket_by_id(db, test_event):
    ticket_data = TicketCreate(
        ticket_number="TICKET123",
        price=50.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    fetched_ticket = get_ticket_by_id(db=db, ticket_id=created_ticket.id)

    assert fetched_ticket is not None
    assert fetched_ticket.id == created_ticket.id
    assert fetched_ticket.ticket_number == "TICKET123"
    assert fetched_ticket.event_id == test_event.id


def test_get_tickets_by_event_id(db, test_event):
    ticket_data1 = TicketCreate(
        ticket_number="TICKET123",
        price=50.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    ticket_data2 = TicketCreate(
        ticket_number="TICKET124",
        price=60.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    create_ticket(db=db, ticket=ticket_data1)
    create_ticket(db=db, ticket=ticket_data2)

    tickets = get_tickets_by_event_id(db=db, event_id=test_event.id)

    assert len(tickets) == 2
    assert tickets[0].event_id == test_event.id
    assert tickets[1].event_id == test_event.id


def test_update_ticket(db, test_event):
    ticket_data = TicketCreate(
        ticket_number="TICKET123",
        price=50.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    update_data = TicketUpdate(
        price=75.0,
        status=TicketStatus.SOLD,
    )
    updated_ticket = update_ticket(db=db, ticket_id=created_ticket.id, ticket_update=update_data)

    assert updated_ticket is not None
    assert updated_ticket.price == 75.0
    assert updated_ticket.status == TicketStatus.SOLD


def test_delete_ticket(db, test_event):
    ticket_data = TicketCreate(
        ticket_number="TICKET123",
        price=50.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    deleted_ticket = delete_ticket(db=db, ticket_id=created_ticket.id)
    assert deleted_ticket is not None

    fetched_ticket = get_ticket_by_id(db=db, ticket_id=created_ticket.id)
    assert fetched_ticket is None

def test_create_ticket_with_user_and_get_by_user_id(db, test_event, test_user):

    print(f"testuser:{test_user.id}")
    ticket_data = TicketCreate(
        ticket_number="TICKET125",
        price=100.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=test_user.id, 
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    results = get_tickets_by_user_id(db=db, user_id=test_user.id)

    assert len(results) == 1
    assert results[0].id == created_ticket.id
    assert results[0].user_id == test_user.id
    assert results[0].event_id == test_event.id
    assert results[0].ticket_number == "TICKET125"
    assert results[0].price == 100.0
    assert results[0].status == TicketStatus.AVAILABLE