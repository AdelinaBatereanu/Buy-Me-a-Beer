from fastapi import APIRouter, HTTPException, Depends, Request
import stripe 
from sqlalchemy.orm import Session

from src.config import settings
from src.schemas import DonationCreate
from src.db import get_db

router = APIRouter(prefix="/payments", tags=["payments"])

stripe.api_key = settings.stripe_secret_key

@router.get("/health-check")
def payments_health():
    return {"status": "payments router up"}

@router.post("/create-checkout-session/")
def create_checkout_session(
    d: DonationCreate,
    db: Session = Depends(get_db)
):
    try:
        # 1) Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": "Buy a Coffee ☕"},
                    "unit_amount": int(d.amount * 100),  # amount in cents
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/cancel",
            metadata={
                "user_name": d.user_name,
                "user_email":      d.email,
                "message":    d.message or ""
            }
        )
        # 2) Return the URL for the client to redirect to
        return {"url": session.url}
    except Exception as e:
        # If something goes wrong on Stripe’s side, return a 500
        raise HTTPException(status_code=500, detail=f"Stripe error: {e}")