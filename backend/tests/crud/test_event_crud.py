import pytest
from app.schemas.event import EventCreate, EventUpdate
from app.crud.event import (
    create_event,
    get_event_by_id,
    get_all_events,
    update_event,
    delete_event,
)


def test_create_event(db):
    event_data = EventCreate(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )

    result = create_event(db=db, event=event_data)

    assert result.id is not None
    assert result.title == "Test Event"
    assert result.description == "This is a test event."
    assert result.location == "Test Location"
    assert result.event_date.isoformat() == "2025-12-01T10:00:00"
    assert result.total_tickets == 100
    assert result.available_tickets == 100


def test_get_event_by_id(db):
    event_data = EventCreate(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )
    created_event = create_event(db=db, event=event_data)

    fetched_event = get_event_by_id(db=db, event_id=created_event.id)

    assert fetched_event is not None
    assert fetched_event.id == created_event.id
    assert fetched_event.title == "Test Event"
    assert fetched_event.description == "This is a test event."


def test_get_all_events(db):
    event_data1 = EventCreate(
        title="Event 1",
        description="Description 1",
        location="Location 1",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )
    event_data2 = EventCreate(
        title="Event 2",
        description="Description 2",
        location="Location 2",
        event_date="2025-12-02T10:00:00Z",
        total_tickets=200,
        available_tickets=200,
    )
    create_event(db=db, event=event_data1)
    create_event(db=db, event=event_data2)

    events = get_all_events(db=db)

    assert len(events) == 2
    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"


def test_update_event(db):
    event_data = EventCreate(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )
    created_event = create_event(db=db, event=event_data)

    update_data = EventUpdate(
        title="Updated Event",
        description="This is an updated event.",
        location="Updated Location",
        total_tickets=150,
        available_tickets=150,
    )
    updated_event = update_event(db=db, event_id=created_event.id, event_update=update_data)

    assert updated_event is not None
    assert updated_event.title == "Updated Event"
    assert updated_event.description == "This is an updated event."
    assert updated_event.location == "Updated Location"
    assert updated_event.total_tickets == 150
    assert updated_event.available_tickets == 150


def test_delete_event(db):
    event_data = EventCreate(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date="2025-12-01T10:00:00Z",
        total_tickets=100,
        available_tickets=100,
    )
    created_event = create_event(db=db, event=event_data)

    deleted_event = delete_event(db=db, event_id=created_event.id)
    assert deleted_event is not None

    fetched_event = get_event_by_id(db=db, event_id=created_event.id)
    assert fetched_event is None