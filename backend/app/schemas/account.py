"""Pydantic schemas for API requests/responses."""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class AccountStatusEnum(str, Enum):
    """Account status values."""
    PENDING_KYC = "pending_kyc"
    ACTIVE = "active"
    FROZEN = "frozen"
    EXPIRED = "expired"
    CLOSED = "closed"


class CreateBurnerAccountRequest(BaseModel):
    """Request to create a burner account."""
    account_holder_name: str = Field(..., min_length=2, max_length=255)
    ttl_days: Optional[int] = Field(None, ge=1, le=90)
    creation_ip: Optional[str] = None
    creation_device_fingerprint: Optional[str] = None


class BurnerAccountResponse(BaseModel):
    """Burner account response."""
    id: str
    account_number: str
    routing_number: str
    account_holder_name: str
    status: AccountStatusEnum
    balance: float
    available_balance: float
    created_at: datetime
    expires_at: datetime
    ttl_days: int
    days_until_expiry: int
    risk_score: int
    is_high_risk: bool
    is_flagged_for_review: bool

    class Config:
        from_attributes = True


class AccountDetailResponse(BurnerAccountResponse):
    """Detailed account response with additional fields."""
    stripe_account_id: Optional[str] = None
    plaid_account_id: Optional[str] = None
    creation_ip: Optional[str] = None
    closed_at: Optional[datetime] = None
    reason_for_closure: Optional[str] = None


class KYCSubmissionRequest(BaseModel):
    """Submit KYC verification for an account."""
    full_name: str = Field(..., min_length=2, max_length=255)
    date_of_birth: str = Field(..., description="YYYY-MM-DD format")
    country: str = Field(..., min_length=2, max_length=2)
    document_type: str = Field(..., description="e.g., 'passport', 'driver_license'")
    document_number: str
    document_expiry: str = Field(..., description="YYYY-MM-DD format")


class KYCVerificationResponse(BaseModel):
    """KYC verification status response."""
    id: str
    account_id: str
    status: str
    is_verified: bool
    verification_timestamp: Optional[datetime] = None
    failure_reason: Optional[str] = None
    retry_count: int
    max_retries: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TransactionRequest(BaseModel):
    """Create a transaction."""
    type: str = Field(..., description="deposit, withdrawal, transfer_in, transfer_out")
    amount: float = Field(..., gt=0)
    counterparty_name: Optional[str] = None
    counterparty_account: Optional[str] = None
    counterparty_routing: Optional[str] = None
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    """Transaction response."""
    id: str
    account_id: str
    type: str
    status: str
    amount: float
    currency: str
    transaction_reference: str
    counterparty_name: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    is_flagged: bool
    flag_reason: Optional[str] = None

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    status_code: int
