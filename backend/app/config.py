"""Application configuration and settings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "sqlite:///./bankofveyda.db"
    database_echo: bool = False

    # FastAPI
    debug: bool = True
    secret_key: str = "dev-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Sandbox APIs
    stripe_api_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    onfido_api_token: Optional[str] = None
    onfido_sandbox_url: str = "https://api.sandbox.onfido.com"
    plaid_client_id: Optional[str] = None
    plaid_secret: Optional[str] = None
    plaid_env: str = "sandbox"

    # Twilio
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_from_number: Optional[str] = None

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
