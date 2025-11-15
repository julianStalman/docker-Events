from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from enums.UserRole import UserRole


def create_user(*, db: Session, user: UserCreate):

    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=get_password_hash(user.password),
        role=user.role,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(*, db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()


def authenticate_user(*, db: Session, email: str, password: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None

    if not verify_password(password, str(db_user.hashed_password)):
        return None

    return db_user


def get_user_by_email(*, db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
