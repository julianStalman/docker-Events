import pytest
from app.schemas.ticket import TicketCreate, TicketUpdateDetails, TicketBuy
from app.crud.ticket import (
    create_ticket,
    get_ticket_by_id,
    get_tickets_by_event_id,
    get_tickets_by_user_id,
    update_ticket_details,
    buy_ticket,
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


def test_buy_ticket(db, test_event, test_admin):
    ticket_data = TicketCreate(
        ticket_number="TICKET124",
        price=60.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    bought_ticket = buy_ticket(db=db, ticket_id=created_ticket.id, user_id=test_admin.id)

    assert bought_ticket.user_id == test_admin.id
    assert bought_ticket.status == TicketStatus.SOLD


def test_buy_ticket_already_sold(db, test_event, test_admin):
    ticket_data = TicketCreate(
        ticket_number="TICKET125",
        price=70.0,
        status=TicketStatus.SOLD,
        event_id=test_event.id,
        user_id=test_admin.id,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    with pytest.raises(ValueError, match="Ticket with ID .* is already sold."):
        buy_ticket(db=db, ticket_id=created_ticket.id, user_id=test_admin.id)


def test_buy_ticket_user_not_found(db, test_event):
    ticket_data = TicketCreate(
        ticket_number="TICKET126",
        price=80.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    with pytest.raises(ValueError, match="User with ID .* does not exist."):
        buy_ticket(db=db, ticket_id=created_ticket.id, user_id=999)


def test_update_ticket_details(db, test_event):
    ticket_data = TicketCreate(
        ticket_number="TICKET127",
        price=90.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    update_data = TicketUpdateDetails(
        price=100.0,
        status=TicketStatus.CANCELLED,
    )
    updated_ticket = update_ticket_details(db=db, ticket_id=created_ticket.id, ticket_update=update_data)

    assert updated_ticket.price == 100.0
    assert updated_ticket.status == TicketStatus.CANCELLED


def test_delete_ticket(db, test_event):
    ticket_data = TicketCreate(
        ticket_number="TICKET128",
        price=100.0,
        status=TicketStatus.AVAILABLE,
        event_id=test_event.id,
        user_id=None,
    )
    created_ticket = create_ticket(db=db, ticket=ticket_data)

    deleted_ticket = delete_ticket(db=db, ticket_id=created_ticket.id)
    assert deleted_ticket is not None

    fetched_ticket = get_ticket_by_id(db=db, ticket_id=created_ticket.id)
    assert fetched_ticket is None