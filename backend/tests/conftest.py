import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.session import Base
from app.api.deps import get_db
from app.main import app
from app.core.security import get_password_hash
from passlib.context import CryptContext
from datetime import datetime, timezone
from app.api.deps import get_current_user

from app.models.user import User
from app.models.ticket import Ticket
from app.models.event import Event
from app.enum.UserRole import UserRole  

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
def create_test_user(db, username: str, email: str, role: UserRole):
    
    user = User(
        username=username,
        email=email,
        role=role,
        hashed_password=hash_password("testpassword"),
        created_at=datetime.now(timezone.utc)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_admin(db):
    return create_test_user(db, username="superuser", email="superuser@example.com", role=UserRole.admin)


@pytest.fixture
def test_admin(db):
    """Fixture to create a test user in the database."""
    hashed_password = get_password_hash("password123")
    user = User(
        email="testuser@example.com",
        name="Test User",
        hashed_password=hashed_password,
        role="admin",
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


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)



def create_client_with_user(client, user):
    def override_get_current_user():
        return user
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def client_with_admin(client, test_admin):
    return create_client_with_user(client, test_admin)