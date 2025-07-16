import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.crud import get_donation_by_id, create_pending_donation, complete_donation

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new in-memory SQLite database for each test function.
    Yields a SQLAlchemy session connected to this database.
    """
    # Create an in-memory SQLite engine
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    # Create a configured "Session" class
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    # Create a new session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_pending_donation(db_session):
    donation = create_pending_donation(db_session, donor_name="Alice", amount=2.5, message="Cheers!")
    assert donation.id is not None
    assert donation.donor_name == "Alice"
    assert donation.amount == 2.5
    assert donation.message == "Cheers!"
    assert donation.status == "pending"

def test_complete_donation(db_session):
    donation = create_pending_donation(db_session, donor_name="Bob", amount=1.0, message=None)
    completed = complete_donation(db_session, donation.id)
    assert completed.status == "completed"
    # Should not change if called again
    completed2 = complete_donation(db_session, donation.id)
    assert completed2.status == "completed"

def test_get_donation_by_id(db_session):
    donation = create_pending_donation(db_session, donor_name="Carol", amount=5.0, message="Great work!")
    fetched = get_donation_by_id(db_session, donation.id)
    assert fetched is not None
    assert fetched.id == donation.id
    assert fetched.donor_name == "Carol"
    assert fetched.amount == 5.0
    assert fetched.message == "Great work!"