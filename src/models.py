from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional
import uuid
from datetime import datetime

# Base class for all models using SQLAlchemy's declarative system
class Base(DeclarativeBase):
     pass

# Donation model representing a donation record in the database
class Donation(Base):
     __tablename__ = "donation"

     # Unique identifier for each donation, generated as a UUID string
     id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     # Name of the donor
     donor_name: Mapped[str]
     # Amount donated
     amount: Mapped[float]
     # Optional message from the donor
     message: Mapped[Optional[str]]
     # Timestamp of the donation, defaults to current time
     timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
     # Status of the donation, defaults to "pending"
     status: Mapped[str] = mapped_column(default="pending")