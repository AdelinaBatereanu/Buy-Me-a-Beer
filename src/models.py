from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime

from src.utils import DonationIDGenerator, CustomerIDGenerator

class Base(DeclarativeBase):
     pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)

class Donation(Base):
    __tablename__ = "donation"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user_account.id"))
    amount: Mapped[float]
    message: Mapped[Optional[str]]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)