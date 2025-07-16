from pydantic import BaseModel, validator
from datetime import datetime

class Donation(BaseModel):
    id: str
    donor_name: str | None = None
    amount: float
    message: str | None = None
    timestamp: datetime
    status: str

class DonationCreate(BaseModel):
    donor_name: str | None = None
    amount: float
    message: str | None = None

    @validator("message")
    def message_max_length(cls, v):
        if v and len(v) > 300:
            raise ValueError("Message must be at most 1000 characters")
        return v