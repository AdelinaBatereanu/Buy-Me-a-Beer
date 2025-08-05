import aiosmtplib
from email.message import EmailMessage
from .config import settings

async def send_merchant_notification(donor_name: str|None, amount: float, message: str|None):
    msg = EmailMessage()
    msg["From"]    = settings.smtp_user
    msg["To"]      = settings.notify_email
    msg["Subject"] = f"New Donation: €{amount:.2f}"

    body = (
        f"🎉 You’ve received a new donation!\n\n"
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