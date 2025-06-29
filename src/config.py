from pydantic_settings import BaseSettings
from pydantic import AnyUrl, ConfigDict

class Settings(BaseSettings):
    # your database URL
    database_url: AnyUrl
    # debug flag for logging or FastAPI debug mode
    debug: bool = False
    # Stripe credentials
    stripe_secret_key:      str
    stripe_publishable_key: str
    stripe_webhook_secret:  str

    model_config = ConfigDict(
        env_file="src/.env",
        env_file_encoding="utf-8"
    )


settings = Settings()