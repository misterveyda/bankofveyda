"""AuditLog model - Compliance audit trail."""

from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.database import Base


class AuditLog(Base):
    """
    Immutable compliance audit trail.
    Demonstrates why anonymity is impossible: every action is logged for regulatory purposes.
    """

    __tablename__ = "audit_logs"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Account Reference
    account_id = Column(String(36), ForeignKey("burner_accounts.id"), nullable=True, index=True)

    # Event Details
    event_type = Column(String(100), nullable=False, index=True)  # e.g., "account_created", "kyc_submitted"
    event_description = Column(Text, nullable=False)

    # User Context
    user_ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(String(500), nullable=True)
    device_fingerprint = Column(String(255), nullable=True)

    # Request/Response Data
    request_data = Column(JSON, nullable=True)
    response_data = Column(JSON, nullable=True)

    # Severity
    severity = Column(String(20), default="INFO", nullable=False)  # INFO, WARNING, ERROR, CRITICAL

    # Timestamp
    timestamp = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<AuditLog {self.event_type} at {self.timestamp}>"
