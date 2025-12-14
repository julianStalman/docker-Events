from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.ticket import (
    create_ticket,
    get_ticket_by_id,
    get_tickets_by_event_id,
    get_tickets_by_user_id,
    update_ticket_details,
    buy_ticket,
    delete_ticket,
)
from app.schemas.ticket import Ticket, TicketCreate, TicketBuy, TicketUpdateDetails
from app.models.user import User 
from app.api.deps import SessionDep, get_current_user, get_current_admin, get_current_organizer, get_current_user_with_ticket_event_access

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=Ticket, dependencies=[Depends(get_current_organizer)])
def create_new_ticket(db: SessionDep, ticket: TicketCreate):
    """
    Create a new ticket.

    Args:
        db (SessionDep): Database session dependency.
        ticket (TicketCreate): Ticket creation schema.

    Returns:
        Ticket: The created ticket.
    """
    try:
        return create_ticket(db=db, ticket=ticket)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the ticket: {str(e)}",
        )
@router.get("/me", response_model=List[Ticket])
def get_my_tickets(db: SessionDep, current_user: User = Depends(get_current_user)):
    """
    Retrieve all tickets for the currently authenticated user.
    """
    tickets = get_tickets_by_user_id(db=db, user_id=current_user.id)

    if not tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tickets found for this user.",
        )

    return tickets

@router.get("/{ticket_id}", response_model=Ticket, dependencies=[Depends(get_current_user_with_ticket_event_access)])
def get_ticket(db: SessionDep, ticket_id: int):
    """
    Retrieve a ticket by its ID.

    Args:
        db (SessionDep): Database session dependency.
        ticket_id (int): ID of the ticket to retrieve.

    Returns:
        Ticket: The retrieved ticket.
    """
    ticket = get_ticket_by_id(db=db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    return ticket


@router.get("/event/{event_id}", response_model=List[Ticket], dependencies=[Depends(get_current_user)])
def get_tickets_for_event(db: SessionDep, event_id: int):
    """
    Retrieve all tickets for a specific event.

    Args:
        db (SessionDep): Database session dependency.
        event_id (int): ID of the event.

    Returns:
        List[Ticket]: A list of tickets for the event.
    """
    tickets = get_tickets_by_event_id(db=db, event_id=event_id)
    if not tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tickets found for this event.",
        )
    return tickets






@router.put("/{ticket_id}/buy", response_model=Ticket)
def buy_ticket_route(db: SessionDep, ticket_id: int, current_user: User = Depends(get_current_user)):
    """
    Buy a ticket for the currently authenticated user.
    """
    try:
        updated_ticket = buy_ticket(
            db=db,
            ticket_id=ticket_id,
            user_id=current_user.id,
        )

        if not updated_ticket:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket is not available or does not exist.",
            )

        return updated_ticket

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )



@router.put("/{ticket_id}/details", response_model=Ticket, dependencies=[Depends(get_current_organizer)])
def update_ticket_details_route(db: SessionDep, ticket_id: int, ticket_update: TicketUpdateDetails):
    """
    Update ticket details such as price and status.

    Args:
        db (SessionDep): Database session dependency.
        ticket_id (int): ID of the ticket to update.
        ticket_update (TicketUpdateDetails): Ticket update schema.

    Returns:
        Ticket: The updated ticket.
    """
    try:
        updated_ticket = update_ticket_details(db=db, ticket_id=ticket_id, ticket_update=ticket_update)
        if not updated_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )
        return updated_ticket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the ticket: {str(e)}",
        )


@router.delete("/{ticket_id}", response_model=Ticket, dependencies=[Depends(get_current_organizer)])
def delete_existing_ticket(db: SessionDep, ticket_id: int):
    """
    Delete an existing ticket.

    Args:
        db (SessionDep): Database session dependency.
        ticket_id (int): ID of the ticket to delete.

    Returns:
        Ticket: The deleted ticket.
    """
    try:
        deleted_ticket = delete_ticket(db=db, ticket_id=ticket_id)
        if not deleted_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )
        return deleted_ticket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the ticket: {str(e)}",
        )