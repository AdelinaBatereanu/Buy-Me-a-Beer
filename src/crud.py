from sqlalchemy.orm import Session
from . import models
from typing import Optional

# def create_user(db: Session, name: str, email: str) -> models.User:
#     user = models.User(name=name, email=email)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
#     return db.query(models.User).filter(models.User.email == email).first()

def create_pending_donation(
    db: Session,
    donor_name: str | None,
    email: str | None,
    amount: float,
    message: str | None
) -> models.Donation:
    """Insert a Donation with status='pending' and return it."""
    donation = models.Donation(
        donor_name=donor_name,
        email=email,
        amount=amount,
        message=message,
        status="pending"
    )
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

def create_donation(db: Session, donor_name: str, email: str, amount: float,  message: str | None = None, status: str = "pending") -> models.Donation:
    donation = models.Donation(donor_name=donor_name, email=email, amount=amount, message=message, status=status)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

def complete_donation(
    db: Session,
    donation_id: str
) -> models.Donation | None:
    """Mark an existing pending Donation as completed."""
    donation = db.get(models.Donation, donation_id)
    if donation:
        donation.status = "completed"
        db.commit()
        db.refresh(donation)
    return donation

def get_donation_by_id(db: Session, donation_id: str) -> models.Donation:
    return db.get(models.Donation, donation_id)

# def list_user_donations(db: Session, user_id: int) -> list[models.User]:
#     return db.query(models.Donation).filter(models.Donation.user_id == user_id).all()