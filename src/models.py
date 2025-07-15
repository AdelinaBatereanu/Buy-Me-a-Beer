from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional
import uuid
from datetime import datetime

from src.utils import DonationIDGenerator, CustomerIDGenerator

class Base(DeclarativeBase):
     pass

class Donation(Base):
    __tablename__ = "donation"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    donor_name: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    amount: Mapped[float]
    message: Mapped[Optional[str]]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    status: Mapped[str] = mapped_column(default="pending")