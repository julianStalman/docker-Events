from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.ticket import (
    create_ticket,
    get_ticket_by_id,
    get_tickets_by_event_id,
    get_tickets_by_user_id,
    update_ticket,
    delete_ticket,
)
from app.schemas.ticket import Ticket, TicketCreate, TicketUpdate
from app.api.deps import SessionDep

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=Ticket)
def create_new_ticket(db: SessionDep, ticket: TicketCreate):
    return create_ticket(db=db, ticket=ticket)


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(db: SessionDep, ticket_id: int):
    ticket = get_ticket_by_id(db=db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    return ticket


@router.get("/event/{event_id}", response_model=List[Ticket])
def get_tickets_for_event(db: SessionDep, event_id: int):
    tickets = get_tickets_by_event_id(db=db, event_id=event_id)
    if not tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tickets found for this event.",
        )
    return tickets


@router.get("/user/{user_id}", response_model=List[Ticket])
def get_tickets_for_user(db: SessionDep, user_id: int):
    tickets = get_tickets_by_user_id(db=db, user_id=user_id)
    if not tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tickets found for this user.",
        )
    return tickets


@router.put("/{ticket_id}", response_model=Ticket)
def update_existing_ticket(db: SessionDep, ticket_id: int, ticket_update: TicketUpdate):
    updated_ticket = update_ticket(db=db, ticket_id=ticket_id, ticket_update=ticket_update)
    if not updated_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    return updated_ticket


@router.delete("/{ticket_id}", response_model=Ticket)
def delete_existing_ticket(db: SessionDep, ticket_id: int):
    deleted_ticket = delete_ticket(db=db, ticket_id=ticket_id)
    if not deleted_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    return deleted_ticket