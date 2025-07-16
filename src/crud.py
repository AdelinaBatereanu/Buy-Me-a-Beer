from sqlalchemy.orm import Session
from . import models
from typing import Optional

def create_pending_donation(
    db: Session,
    donor_name: Optional[str],
    amount: float,
    message: Optional[str]
) -> models.Donation:
    """
    Create and insert a new Donation with status='pending'.

    Args:
        db (Session): SQLAlchemy database session.
        donor_name (Optional[str]): Name of the donor.
        amount (float): Donation amount.
        message (Optional[str]): Optional message from the donor.

    Returns:
        models.Donation: The newly created Donation object.
    """
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
) -> Optional[models.Donation]:
    """
    Mark an existing pending Donation as completed.

    Args:
        db (Session): SQLAlchemy database session.
        donation_id (str): The ID of the donation to complete.

    Returns:
        Optional[models.Donation]: The updated Donation object if found, else None.
    """
    donation = db.get(models.Donation, donation_id)
    if donation:
        donation.status = "completed"
        db.commit()
        db.refresh(donation)
    return donation

def get_donation_by_id(
    db: Session,
    donation_id: str
) -> Optional[models.Donation]:
    """
    Retrieve a Donation by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        donation_id (str): The ID of the donation to retrieve.

    Returns:
        Optional[models.Donation]: The Donation object if found, else None.
    """
    return db.get(models.Donation, donation_id)
