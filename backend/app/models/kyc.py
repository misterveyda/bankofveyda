"""KYCVerification model - Identity verification records."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.database import Base


class VerificationStatus(str, PyEnum):
    """KYC verification workflow stages."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    RETRY_REQUESTED = "retry_requested"


class VerificationProvider(str, PyEnum):
    """External KYC providers."""
    ONFIDO = "onfido"
    VERIFF = "veriff"
    COMPLYCUBE = "complycube"


class KYCVerification(Base):
    """
    Know-Your-Customer verification record.
    Educational insight: Why anonymous accounts are impossible - KYC is the bottleneck.
    """

    __tablename__ = "kyc_verifications"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Key to Account
    account_id = Column(String(36), ForeignKey("burner_accounts.id"), nullable=False, index=True)

    # Provider Configuration
    provider = Column(Enum(VerificationProvider), default=VerificationProvider.ONFIDO, nullable=False)
    provider_check_id = Column(String(255), nullable=True, unique=True)

    # Verification Status
    status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False)

    # User Information (PII - encrypted in production)
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(String(10), nullable=False)  # YYYY-MM-DD
    country = Column(String(2), nullable=False)  # ISO 3166-1 alpha-2
    
    # Document Information
    document_type = Column(String(50), nullable=True)  # e.g., "passport", "driver_license"
    document_number = Column(String(100), nullable=True)
    document_expiry = Column(String(10), nullable=True)  # YYYY-MM-DD

    # Verification Details
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_timestamp = Column(DateTime, nullable=True)
    failure_reason = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)

    # Audit Trail
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Raw Response from Provider (for debugging)
    provider_response = Column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<KYCVerification {self.id} - {self.provider} ({self.status})>"
