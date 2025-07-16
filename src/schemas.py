from pydantic import BaseModel
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