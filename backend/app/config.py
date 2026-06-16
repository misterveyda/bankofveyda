"""Application configuration and settings."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str
    database_echo: bool = False

    # FastAPI
    debug: bool = True
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Sandbox APIs
    stripe_api_key: str
    stripe_webhook_secret: str
    onfido_api_token: str
    onfido_sandbox_url: str = "https://api.sandbox.onfido.com"
    plaid_client_id: str
    plaid_secret: str
    plaid_env: str = "sandbox"

    # Twilio
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Account Configuration
    default_account_ttl_days: int = 30
    risk_score_threshold: int = 75
    high_value_transaction_limit: float = 5000.0
    high_value_time_window_hours: int = 1

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
