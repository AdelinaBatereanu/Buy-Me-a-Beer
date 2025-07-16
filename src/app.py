from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from datetime import datetime
import stripe
from typing import List

from src import models
from src.db import SessionLocal, get_db
from src.schemas import Donation, DonationCreate
from src import crud
from src.config import settings
from src.payments import router as payments_router

app = FastAPI(debug=settings.debug)

app.include_router(payments_router)

templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/success", include_in_schema=False)
def read_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/donations/{donation_id}", response_model=Donation)
def get_donation(donation_id: str, db: Session = Depends(get_db)):
    try:
        donation = crud.get_donation_by_id(db, donation_id)
        if not donation:
            raise HTTPException(404, "Donation not found")
        return donation
    except Exception as e:
        raise HTTPException(500, f"Internal server error: {e}")

@app.get("/donations/", response_model=List[Donation])
def list_donations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Donation).offset(skip).limit(limit).all()

@app.get("/cancel", include_in_schema=False)
def read_cancel(request: Request, donation_id: str = None, db: Session = Depends(get_db)):
    if donation_id:
        donation = crud.get_donation_by_id(db, donation_id)
        if donation and donation.status == "pending":
            donation.status = "canceled"
            db.commit()
    return templates.TemplateResponse("cancel.html", {"request": request})

app.mount("/static", StaticFiles(directory="static"), name="static")
