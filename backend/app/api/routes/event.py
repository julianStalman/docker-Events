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
from app.api.deps import SessionDep

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=Event)
def create_new_event(db: SessionDep, event: EventCreate):
    return create_event(db=db, event=event)


@router.get("/{event_id}", response_model=Event)
def get_event(db: SessionDep, event_id: int):
    event = get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return event


@router.get("/", response_model=List[Event])
def list_all_events(db: SessionDep):
    events = get_all_events(db=db)
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No events found.",
        )
    return events


@router.put("/{event_id}", response_model=Event)
def update_existing_event(db: SessionDep, event_id: int, event_update: EventUpdate):
    updated_event = update_event(db=db, event_id=event_id, event_update=event_update)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return updated_event


@router.delete("/{event_id}", response_model=Event)
def delete_existing_event(db: SessionDep, event_id: int):
    deleted_event = delete_event(db=db, event_id=event_id)
    if not deleted_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return deleted_event