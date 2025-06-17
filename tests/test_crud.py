import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.crud import create_user, get_user_by_email, create_donation, get_donation_by_id

@pytest.fixture(scope="function")
def db_session():
    # 1) In-memory SQLite
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # 2) Create tables
    Base.metadata.create_all(bind=engine)
    # 3) Provide a session to tests
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_and_get_user(db_session):
    # Initially, no user
    assert get_user_by_email(db_session, "alice@example.com") is None

    # Create user
    user = create_user(db_session, name="Alice", email="alice@example.com")
    assert user.id is not None
    assert user.name == "Alice"

    # Fetch by email
    fetched = get_user_by_email(db_session, "alice@example.com")
    assert fetched is not None
    assert fetched.id == user.id

def test_create_and_get_donation(db_session):
    assert get_donation_by_id(db_session, "1") is None

    user = create_user(db_session, name="Alice", email="alice@example.com")
    donation = create_donation(db_session, user=user, amount=100.50)
    assert donation.id is not None
    assert donation.amount == 100.50
    assert donation.user_id is not None
    assert donation.timestamp is not None

    fetched = get_donation_by_id(db_session, "1")
    assert fetched is not None
    assert fetched.id == donation.id