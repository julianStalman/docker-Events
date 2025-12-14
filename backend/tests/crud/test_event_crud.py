import pytest
from app.schemas.event import EventCreate, EventUpdate
from app.crud.event import (
    create_event,
    get_event_by_id,
    get_all_events,
    update_event,
    delete_event,
)


def test_create_event_with_tickets(db):
    event_data = EventCreate(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )

    result = create_event(db=db, event=event_data, ticket_price=50.0)

    assert result.id is not None
    assert result.title == "Test Event"
    assert result.total_tickets == 100
    assert result.available_tickets == 100


def test_update_event(db):
    event_data = EventCreate(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )
    created_event = create_event(db=db, event=event_data, ticket_price=50.0)

    update_data = EventUpdate(
        title="Updated Event",
        description="Updated description.",
        total_tickets=150,
    )
    updated_event = update_event(db=db, event_id=created_event.id, event_update=update_data)

    assert updated_event.title == "Updated Event"
    assert updated_event.total_tickets == 150


def test_delete_event(db):
    event_data = EventCreate(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )
    created_event = create_event(db=db, event=event_data, ticket_price=50.0)

    deleted_event = delete_event(db=db, event_id=created_event.id)
    assert deleted_event is not None

    fetched_event = get_event_by_id(db=db, event_id=created_event.id)
    assert fetched_event is None


def test_create_event_with_no_description(db):
    event_data = EventCreate(
        title="Event Without Description",
        description=None,
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=50,
        available_tickets=50,
    )

    result = create_event(db=db, event=event_data, ticket_price=25.0)

    assert result.id is not None
    assert result.title == "Event Without Description"
    assert result.description is None
    assert result.total_tickets == 50
    assert result.available_tickets == 50


def test_get_event_by_invalid_id(db):
    event = get_event_by_id(db=db, event_id=99999)
    assert event is None


def test_get_all_events_empty(db):
    events = get_all_events(db=db)
    assert len(events) == 0


def test_update_event_partial_fields(db):
    event_data = EventCreate(
        title="Event to Partially Update",
        description="Initial Description",
        location="Initial Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )
    created_event = create_event(db=db, event=event_data, ticket_price=50.0)

    update_data = EventUpdate(
        description="Updated Description",
        location="Updated Location",
    )
    updated_event = update_event(db=db, event_id=created_event.id, event_update=update_data)

    assert updated_event.description == "Updated Description"
    assert updated_event.location == "Updated Location"
    assert updated_event.title == "Event to Partially Update"  # Unchanged
    assert updated_event.total_tickets == 100  # Unchanged


def test_delete_event_invalid_id(db):
    deleted_event = delete_event(db=db, event_id=99999)
    assert deleted_event is None


def test_create_event_with_zero_tickets(db):
    event_data = EventCreate(
        title="Event With Zero Tickets",
        description="This event has no tickets.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=0,
        available_tickets=0,
    )

    result = create_event(db=db, event=event_data, ticket_price=0.0)

    assert result.id is not None
    assert result.title == "Event With Zero Tickets"
    assert result.total_tickets == 0
    assert result.available_tickets == 0