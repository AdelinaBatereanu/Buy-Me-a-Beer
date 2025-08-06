from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging

from sqlalchemy.orm import Session
from typing import List

from src import models
from src.db import get_db, SessionLocal
from src.schemas import Donation
from src import crud
from src.config import settings
from src.payments import router as payments_router

# Configure logging globally
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("buy-me-a-beer")

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
    logger.info("Rendering home page")
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/about", include_in_schema=False)
def read_about(request: Request):
    """
    Render the about me page.
    """
    logger.info("Rendering about me page")
    return templates.TemplateResponse(request, "about.html", {})

@app.get("/success", include_in_schema=False)
def read_success(request: Request):
    """
    Render the success page after a successful donation.
    """
    logger.info("Rendering success page")
    return templates.TemplateResponse(request, "success.html", {})

@app.get("/donations/{donation_id}", response_model=Donation)
def get_donation(donation_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a donation by its ID.
    """
    logger.info(f"Fetching donation {donation_id}")
    try:
        donation = crud.get_donation_by_id(db, donation_id)
        if not donation:
            logger.warning(f"Donation {donation_id} not found")
            raise HTTPException(404, "Donation not found")
        logger.info(f"Donation {donation_id} found: status={donation.status}")
        return donation
    except Exception as e:
        raise HTTPException(500, f"Internal server error: {e}")

def require_api_key(x_api_key: str = Header(...)):
    """
    Dependency to require a valid API key for admin endpoints.
    """
    logger.debug("Checking admin API key")
    if x_api_key != settings.admin_api_key:
        logger.warning("Invalid API key attempt")
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
    logger.info(f"Listing donations: skip={skip}, limit={limit}")
    return db.query(models.Donation).offset(skip).limit(limit).all()

@app.get("/cancel", include_in_schema=False)
def read_cancel(request: Request, donation_id: str = None, db: Session = Depends(get_db)):
    """
    Cancel a pending donation if donation_id is provided, then render the cancel page.
    """
    logger.info(f"Cancel page requested for donation_id={donation_id}")
    if donation_id:
        donation = crud.get_donation_by_id(db, donation_id)
        if donation and donation.status == "pending":
            logger.info(f"Canceling pending donation {donation_id}")
            donation.status = "canceled"
            db.commit()
        else:
            logger.info(f"No pending donation to cancel for id={donation_id}")
    return templates.TemplateResponse(request, "cancel.html", {})

def clean_old_donations():
    logger.info("Running background cleanup for old donations")
    db = SessionLocal()
    try:
        threshold = datetime.now() - timedelta(minutes=120)
        deleted = db.query(models.Donation).filter(
            (models.Donation.status == "pending") | (models.Donation.status == "canceled"),
            models.Donation.timestamp < threshold
        ).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Deleted old donations: {deleted}")
    except Exception as e:
        logger.error(f"Error cleaning old donations: {e}")
    finally:
        db.close()

if __name__ == "__main__" or settings.debug:
    logger.info("Starting background scheduler for donation cleanup")
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_old_donations, "interval", minutes=1440)
    scheduler.start()