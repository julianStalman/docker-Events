from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.event import (
    create_event,
    get_event_by_id,
    get_all_events,
    update_event,
    delete_event,
)
from app.schemas.event import Event, EventCreate, EventUpdate
from app.api.deps import SessionDep, get_current_organizer, get_current_admin, get_current_user

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=Event, dependencies=[Depends(get_current_organizer)])
def create_new_event(db: SessionDep, event: EventCreate, ticket_price: float):
    """
    Create a new event and generate tickets for it.

    Args:
        db (SessionDep): Database session dependency.
        event (EventCreate): Event creation schema.
        ticket_price (float): Price for each ticket.

    Returns:
        Event: The created event.
    """
    return create_event(db=db, event=event, ticket_price=ticket_price)


@router.get("/{event_id}", response_model=Event, dependencies=[Depends(get_current_user)])
def get_event(db: SessionDep, event_id: int):
    """
    Retrieve an event by its ID.

    Args:
        db (SessionDep): Database session dependency.
        event_id (int): ID of the event to retrieve.

    Returns:
        Event: The retrieved event.
    """
    event = get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return event


@router.get("/", response_model=List[Event], dependencies=[Depends(get_current_user)])
def list_all_events(db: SessionDep):
    """
    List all events.

    Args:
        db (SessionDep): Database session dependency.

    Returns:
        List[Event]: A list of all events.
    """
    events = get_all_events(db=db)
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No events found.",
        )
    return events


@router.put("/{event_id}", response_model=Event, dependencies=[Depends(get_current_organizer)])
def update_existing_event(db: SessionDep, event_id: int, event_update: EventUpdate):
    """
    Update an existing event.

    Args:
        db (SessionDep): Database session dependency.
        event_id (int): ID of the event to update.
        event_update (EventUpdate): Event update schema.

    Returns:
        Event: The updated event.
    """
    updated_event = update_event(db=db, event_id=event_id, event_update=event_update)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return updated_event


@router.delete("/{event_id}", response_model=Event, dependencies=[Depends(get_current_organizer)])
def delete_existing_event(db: SessionDep, event_id: int):
    """
    Delete an existing event.

    Args:
        db (SessionDep): Database session dependency.
        event_id (int): ID of the event to delete.

    Returns:
        Event: The deleted event.
    """
    deleted_event = delete_event(db=db, event_id=event_id)
    if not deleted_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return deleted_event