import pytest
from app.schemas.user import UserCreate
from app.crud.user import (
    create_user,
    get_user,
    get_users,
    authenticate_user,
    get_user_by_email,
)
from app.models.user import User
from app.core.security import get_password_hash



def test_create_user(db):
    user_data = UserCreate(
        email="testuser@example.com",
        name="Test User",
        password="password123",
        role="user",
    )

    result = create_user(db=db, user=user_data)

    assert result.id is not None
    assert result.email == "testuser@example.com"
    assert result.name == "Test User"
    assert result.role == "user"


def test_get_user(db, test_admin):
    result = get_user(db=db, user_id=test_admin.id)

    assert result.id == test_admin.id
    assert result.email == test_admin.email
    assert result.name == test_admin.name


def test_get_user_not_found(db):
    result = get_user(db=db, user_id=99999)
    assert result is None


def test_get_users(db, test_admin):
    result = get_users(db=db)

    assert any(user.id == test_admin.id for user in result)


def test_authenticate_user(db, test_admin):
    result = authenticate_user(
        db=db, email=test_admin.email, password="password123"
    )

    assert result.id == test_admin.id
    assert result.email == test_admin.email


def test_authenticate_user_invalid_password(db, test_admin):
    result = authenticate_user(
        db=db, email=test_admin.email, password="wrongpassword"
    )

    assert result is None


def test_authenticate_user_not_found(db):
    result = authenticate_user(
        db=db, email="nonexistent@example.com", password="password123"
    )

    assert result is None


def test_get_user_by_email(db, test_admin):
    result = get_user_by_email(db=db, email=test_admin.email)

    assert result.id == test_admin.id
    assert result.email == test_admin.email


def test_get_user_by_email_not_found(db):
    result = get_user_by_email(db=db, email="nonexistent@example.com")
    assert result is None