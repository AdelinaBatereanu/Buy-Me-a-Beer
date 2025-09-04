import aiosmtplib
from email.message import EmailMessage
import logging
from .config import settings
from fastapi import HTTPException, Header

logger = logging.getLogger(__name__)

async def send_merchant_notification(donor_name: str|None, amount: float, message: str|None):
    """Send email notification for new donation"""
    try:
        msg = EmailMessage()
        msg["From"]    = settings.smtp_user
        msg["To"]      = settings.notify_email
        msg["Subject"] = f"Buy Me a Beer - New Donation"

        body = (
            f"🎉 Your work is being rewarded! Someone was generous enough to buy you a beer!\n\n"
            f"Amount: €{amount:.2f}\n"
            f"Donor:   {donor_name or 'Anonymous'}\n"
            f"Message: {message or '<no message>'}\n"
        )
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_pass,
            start_tls=True
        )
        logger.info("Email notification sent successfully")
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        return False

def require_api_key(x_api_key: str = Header(...)):
    """
    Dependency to require a valid API key for admin endpoints.
    """
    logger.debug("Checking admin API key")
    if x_api_key != settings.admin_api_key:
        logger.warning("Invalid API key attempt")
        raise HTTPException(403, "Forbidden: Invalid API Key")