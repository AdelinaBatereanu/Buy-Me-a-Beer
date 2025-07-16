from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from typing import List

from src import models
from src.db import get_db
from src.schemas import Donation
from src import crud
from src.config import settings
from src.payments import router as payments_router

# Initialize FastAPI app with debug setting
app = FastAPI(debug=settings.debug)

# Include payment-related routes
app.include_router(payments_router)

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def root(request: Request):
    """
    Render the home page.
    """
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/success", include_in_schema=False)
def read_success(request: Request):
    """
    Render the success page after a successful donation.
    """
    return templates.TemplateResponse(request, "success.html", {})

@app.get("/donations/{donation_id}", response_model=Donation)
def get_donation(donation_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a donation by its ID.
    """
    try:
        donation = crud.get_donation_by_id(db, donation_id)
        if not donation:
            raise HTTPException(404, "Donation not found")
        return donation
    except Exception as e:
        raise HTTPException(500, f"Internal server error: {e}")

def require_api_key(x_api_key: str = Header(...)):
    """
    Dependency to require a valid API key for admin endpoints.
    """
    if x_api_key != settings.admin_api_key:
        raise HTTPException(403, "Forbidden: Invalid API Key")

@app.get(
    "/donations/",
    response_model=List[Donation],
    dependencies=[Depends(require_api_key)]
)
def list_donations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all donations with pagination. Requires admin API key.
    """
    return db.query(models.Donation).offset(skip).limit(limit).all()

@app.get("/cancel", include_in_schema=False)
def read_cancel(request: Request, donation_id: str = None, db: Session = Depends(get_db)):
    """
    Cancel a pending donation if donation_id is provided, then render the cancel page.
    """
    if donation_id:
        donation = crud.get_donation_by_id(db, donation_id)
        if donation and donation.status == "pending":
            donation.status = "canceled"
            db.commit()
    return templates.TemplateResponse(request, "cancel.html", {})
