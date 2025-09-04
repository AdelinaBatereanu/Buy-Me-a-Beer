from pydantic import BaseModel, field_validator
from datetime import datetime

class Donation(BaseModel):
    """
    Schema for a donation record.
    """
    id: str  # Unique id for the donation
    donor_name: str | None = None  # Optional donor name
    amount: float  # Donation amount
    message: str | None = None  # Optional message from donor
    timestamp: datetime  # Time when the donation was made
    status: str  # Status of the donation ('pending', 'completed', 'canceled')

class DonationCreate(BaseModel):
    """
    Schema for creating a new donation.
    """
    donor_name: str | None = None  # Optional donor name
    amount: float  # Donation amount
    message: str | None = None  # Optional message from donor

    @field_validator("message")
    @classmethod
    def message_max_length(cls, message):
        if message and len(message) > 300:
            raise ValueError("Message must be at most 300 characters")
        return message