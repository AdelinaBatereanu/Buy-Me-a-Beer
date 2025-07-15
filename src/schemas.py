from pydantic import BaseModel, EmailStr
from datetime import datetime

class Donation(BaseModel):
    id: str
    donor_name: str | None = None
    email: str | None = None
    amount: float
    message: str | None = None
    timestamp: datetime
    status: str

class DonationCreate(BaseModel):
    donor_name: str | None = None
    email: EmailStr | None = None
    amount: float
    message: str | None = None