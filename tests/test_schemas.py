import pytest
from src.schemas import DonationCreate

def test_donation_create_message_length():
    # Valid message
    DonationCreate(donor_name="Test", amount=1.0, message="a" * 300)
    # Invalid message
    with pytest.raises(ValueError):
        DonationCreate(donor_name="Test", amount=1.0, message="a" * 301)