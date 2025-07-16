from fastapi import APIRouter, HTTPException, Depends, Request
import stripe 
from sqlalchemy.orm import Session
import logging

from src.config import settings
from src.schemas import DonationCreate
from src.db import get_db
from src.crud import create_pending_donation, complete_donation

router = APIRouter(prefix="/payments", tags=["payments"])

stripe.api_key = settings.stripe_secret_key

@router.post("/create-checkout-session/")
def create_checkout_session(
    d: DonationCreate,
    db: Session = Depends(get_db)
):
    try:
        logging.info(f"Creating pending donation for {d.donor_name}, amount: {d.amount}")
        pending = create_pending_donation(db, d.donor_name, d.amount, d.message)
        # 1) Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": "Buy Me a Beer"},
                    "unit_amount": int(d.amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"http://localhost:8000/success?donation_id={pending.id}&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"http://localhost:8000/cancel?donation_id={pending.id}",
            metadata={
                "donor_name": d.donor_name,
                "message":    d.message or "",
                "donation_id": str(pending.id)
            }
        )
        logging.info(f"Stripe session created: {session.id} for donation {pending.id}")
        # 2) Return the URL for the client to redirect to
        return {"url": session.url}
    except stripe.error.StripeError as e:
        logging.error(f"Stripe API error: {e.user_message or str(e)}")
        raise HTTPException(status_code=502, detail=f"Stripe error: {e.user_message or str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in create-checkout-session: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.post("/webhook/")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    logging.info("Webhook endpoint called")
    # 1) Read the raw body and Stripe-Signature header
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    # 2) Verify the event came from Stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError as e:
        logging.error(f"Invalid payload: {e}")
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logging.error(f"Invalid signature: {e}")
        raise HTTPException(400, "Invalid signature")
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        raise HTTPException(400, str(e))
    logging.info(f"Stripe event type: {event['type']}")

    # 3) Handle the event type
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Extract the information we put in metadata
        donation_id = session["metadata"].get("donation_id", "")

        # 4) Create the donation with status completed
        try:
            logging.info(f"Completing donation {donation_id}")
            complete_donation(db, donation_id)
            logging.info(f"Donation {donation_id} marked as completed")
        except Exception as e:
            print("Error completing donation:", e)
            logging.error(f"Error completing donation: {e}")

    # 5) Return a 200 to acknowledge receipt
    return {"status": "success"}