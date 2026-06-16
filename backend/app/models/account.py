"""BurnerAccount model - temporary financial identity."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, Enum
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from enum import Enum as PyEnum
import uuid

from app.database import Base
from app.config import get_settings


class AccountStatus(str, PyEnum):
    """Account lifecycle statuses."""
    PENDING_KYC = "pending_kyc"
    ACTIVE = "active"
    FROZEN = "frozen"
    EXPIRED = "expired"
    CLOSED = "closed"


class BurnerAccount(Base):
    """
    Temporary financial account with Time-To-Live (TTL).
    Demonstrates why truly anonymous accounts don't exist legally.
    """

    __tablename__ = "burner_accounts"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Account Identity
    account_number = Column(String(17), unique=True, nullable=False, index=True)
    routing_number = Column(String(9), nullable=False)
    account_holder_name = Column(String(255), nullable=False)

    # Account Status
    status = Column(Enum(AccountStatus), default=AccountStatus.PENDING_KYC, nullable=False)
    
    # Financial Data
    balance = Column(Float, default=0.0, nullable=False)
    available_balance = Column(Float, default=0.0, nullable=False)
    
    # Time-To-Live Configuration
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    ttl_days = Column(Integer, nullable=False)
    
    # External API References
    stripe_account_id = Column(String(255), unique=True, nullable=True)
    plaid_account_id = Column(String(255), unique=True, nullable=True)
    
    # Risk & Compliance
    risk_score = Column(Integer, default=0, nullable=False)
    is_high_risk = Column(Boolean, default=False, nullable=False)
    is_flagged_for_review = Column(Boolean, default=False, nullable=False)
    
    # Device & IP Tracking (for audit trail)
    creation_ip = Column(String(45), nullable=True)  # IPv6 compatible
    creation_device_fingerprint = Column(String(255), nullable=True)
    
    # Metadata
    reason_for_closure = Column(Text, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, account_holder_name: str, ttl_days: int = None, **kwargs):
        """Initialize burner account with TTL."""
        settings = get_settings()
        if ttl_days is None:
            ttl_days = settings.default_account_ttl_days
        
        self.ttl_days = ttl_days
        self.expires_at = datetime.utcnow() + timedelta(days=ttl_days)
        self.account_holder_name = account_holder_name
        super().__init__(**kwargs)

    @property
    def is_expired(self) -> bool:
        """Check if account has passed its TTL."""
        return datetime.utcnow() > self.expires_at

    @property
    def days_until_expiry(self) -> int:
        """Days remaining before account expiration."""
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)

    def __repr__(self) -> str:
        return f"<BurnerAccount {self.account_number} ({self.status})>"
