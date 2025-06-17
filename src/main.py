from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Generator

from src.db import SessionLocal
from src.schemas import User, Donation, DonationCreate
from src import crud

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def read_root():
    return {"status": "ok", "service": "BuyMeACoffee"}

@app.get("/donate/{donation_id}", response_model=Donation)
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = crud.get_donation_by_id(db, donation_id)
    if not donation:
        raise HTTPException(404, "Donation not found")
    return donation

@app.post("/donate/", response_model=Donation)
def donate(user_input: DonationCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_input.user_email)
    if not user:
       user = crud.create_user(db, user_input.user_name, user_input.user_email)

    donation = crud.create_donation(db, user, user_input.amount, user_input.message)
    return donation

