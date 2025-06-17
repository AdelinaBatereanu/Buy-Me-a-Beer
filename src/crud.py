from sqlalchemy.orm import Session
from . import models
from typing import Optional

def create_user(db: Session, name: str, email: str) -> models.User:
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_donation(db: Session, user: models.User, amount: float,  message: str | None = None) -> models.Donation:
    donation = models.Donation(user_id=user.id, amount=amount, message=message)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

def get_donation_by_id(db: Session, donation_id: int) -> models.Donation:
    return db.get(models.Donation, donation_id)

def list_user_donations(db: Session, user_id: int) -> list[models.User]:
    return db.query(models.Donation).filter(models.Donation.user_id == user_id).all()