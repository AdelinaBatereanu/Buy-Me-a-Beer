from fastapi import APIRouter, HTTPException, Depends, Request
import stripe 
from sqlalchemy.orm import Session
import logging
import os

from src.config import settings
from src.schemas import DonationCreate
from src.db import get_db
from src.crud import create_donation

router = APIRouter(prefix="", tags=["payments"])

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
                    "product_data": {"name": "Buy Me a Beer"},
                    "unit_amount": int(d.amount * 100),  # amount in cents
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
            # success_url="http://localhost:8000/donations/",
            cancel_url="http://localhost:8000/index",
            metadata={
                "donor_name": d.donor_name or "",
                "email":      d.email or "",
                "message":    d.message or ""
            }
        )
        # 2) Return the URL for the client to redirect to
        return {"url": session.url}
    except Exception as e:
        # If something goes wrong on Stripe’s side, return a 500
        raise HTTPException(status_code=500, detail=f"Stripe error: {e}")
    

@router.post("/webhook/")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    print("Webhook endpoint called")
    # 1) Read the raw body and Stripe-Signature header
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    # 2) Verify the event came from Stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        raise HTTPException(400, str(e))
    except ValueError:
        # Invalid payload
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise HTTPException(400, "Invalid signature")
    print("Stripe event type:", event["type"])

    # 3) Handle the event type
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Extract the information we put in metadata
        donor_name = session["metadata"]["donor_name"] or None
        email     = session["metadata"]["email"] or None
        message   = session["metadata"]["message"] or None
        amount    = session["amount_total"] / 100

        # 4) Create the donation with status completed
        try:
            print("Creating donation...")
            create_donation(db, donor_name, email, amount, message, status="completed")
            print("Donation created!")
        except Exception as e:
            print("Error creating donation:", e)
            logging.error(f"Error creating donation: {e}")

    # 5) Return a 200 to acknowledge receipt
    return {"status": "success"}