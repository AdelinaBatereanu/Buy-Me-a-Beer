from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

class Donation(BaseModel):
    id: int
    user_id: int
    amount: float
    message: str | None = None
    timestamp: datetime

class DonationCreate(BaseModel):
    user_email: EmailStr
    user_name: str
    amount: float
    message: str | None = None
    