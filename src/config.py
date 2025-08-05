from pydantic_settings import BaseSettings
from pydantic import AnyUrl, ConfigDict, EmailStr

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    # Database connection URL
    database_url: AnyUrl

    # Enable or disable debug mode
    debug: bool = False

    # Stripe API credentials
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str

    # Admin API key for privileged operations
    admin_api_key: str

    # SMTP settings for sending emails
    smtp_host:     str
    smtp_port:     int
    smtp_user:     str
    smtp_pass:     str
    notify_email:  EmailStr

    # Pydantic model configuration for environment file support
    model_config = ConfigDict(
        env_file=".env",            # Load variables from .env file
        env_file_encoding="utf-8"   # Use UTF-8 encoding for .env file
    )

# Instantiate settings; values are loaded from environment or .env file
settings = Settings()