import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.session import Base
from app.api.deps import get_db
from app.main import app
from app.core.security import get_password_hash
from passlib.context import CryptContext
from datetime import datetime

from app.models.user import User
from app.models.ticket import Ticket
from app.models.event import Event  

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Test database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@pytest.fixture(scope="function")
def db():
    """Fixture to provide a database session for tests."""
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop the database tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(db):
    """Fixture to create a test user in the database."""
    hashed_password = get_password_hash("password123")
    user = User(
        email="testuser@example.com",
        name="Test User",
        hashed_password=hashed_password,
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_event(db):
    event = Event(
        title="Test Event",
        description="This is a test event.",
        location="Test Location",
        event_date=datetime.utcnow(),
        total_tickets=100,
        available_tickets=100,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    print(f"Test Event ID: {event.id}") 
    return event

@pytest.fixture
def test_event_data():
    return {
        "title": "Test Event",
        "description": "This is a test event.",
        "date": "2023-10-01",
        "location": "Test Location",
    }