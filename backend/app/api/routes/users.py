from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.user import (
    create_user,
    get_user,
    get_users,
    get_user_by_email,
    authenticate_user,
)
from app.schemas.user import User, UserCreate
from app.api.deps import SessionDep, get_current_admin


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=User, dependencies=[Depends(get_current_admin)])
def register_user(db: SessionDep, user: UserCreate):
    existing_user = get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    return create_user(db=db, user=user)


@router.get("/{user_id}", response_model=User)
def get_user_by_id(db: SessionDep, user_id: int):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.get("/", response_model=List[User])
def list_users(db: SessionDep):
    return get_users(db=db)


@router.post("/login", response_model=User)
def login_user(db: SessionDep, email: str, password: str):
    user = authenticate_user(db=db, email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return user