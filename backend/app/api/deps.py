from collections.abc import Generator
from typing import Annotated

from sqlalchemy.orm import Session

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.database.session import engine
from app.core import security
from app.core.config import settings

from app.schemas.token import TokenData
from app.schemas.user import User, UserRole
from app.crud.user import get_user_by_email
from app.crud.event import get_event_by_id



# Database Session
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session.

    This function is a generator that yields a SQLAlchemy session object.
    It ensures that the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy session object.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

# Security
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Retrieve the current user based on the provided session and token.

    Args:
        session (SessionDep): The database session dependency.
        token (TokenDep): The JWT token dependency.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid, credentials cannot be validated,
                       the user is not found, or the user is inactive.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        token_data = TokenData(username=username)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    assert token_data.username is not None
    user = get_user_by_email(db=session, email=token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.updated_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_admin(current_user: CurrentUser) -> User:

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges to access this resource",
        )
    return current_user


def get_current_organizer(current_user: CurrentUser) -> User:

    if current_user.role != UserRole.ORGANIZER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges to access this resource",
        )
    return current_user


def get_current_user_with_event_access(
    current_user: CurrentUser, event_id: int, session: SessionDep
) -> User:

    event = get_event_by_id(db=session, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )

    if (
        current_user.role == UserRole.ADMIN
        or (current_user.role == UserRole.ORGANIZER and event.organizer_id == current_user.id)
        or any(ticket.event_id == event_id for ticket in current_user.tickets)
    ):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user doesn't have access to this event.",
    )