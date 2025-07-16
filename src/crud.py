from sqlalchemy.orm import Session
from . import models
from typing import Optional

def create_pending_donation(
    db: Session,
    donor_name: str | None,
    amount: float,
    message: str | None
) -> models.Donation:
    """Insert a Donation with status='pending' and return it."""
    donation = models.Donation(
        donor_name=donor_name,
        amount=amount,
        message=message,
        status="pending"
    )
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
