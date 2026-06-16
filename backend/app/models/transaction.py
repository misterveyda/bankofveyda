"""Transaction model - Financial transactions."""

from sqlalchemy import Column, String, DateTime, Float, Text, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.database import Base


class TransactionType(str, PyEnum):
    """Transaction classification."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"
    CLOSURE_RETURN = "closure_return"
    REVERSAL = "reversal"


class TransactionStatus(str, PyEnum):
    """Transaction lifecycle."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"
    FLAGGED = "flagged"


class Transaction(Base):
    """
    Financial transaction record.
    Immutable audit trail for compliance.
    """

    __tablename__ = "transactions"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Key
    account_id = Column(String(36), ForeignKey("burner_accounts.id"), nullable=False, index=True)

    # Transaction Details
    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)

    # Counter Party
    counterparty_name = Column(String(255), nullable=True)
    counterparty_account = Column(String(255), nullable=True)
    counterparty_routing = Column(String(9), nullable=True)

    # Transaction Reference
    transaction_reference = Column(String(255), unique=True, nullable=False, index=True)
    external_reference = Column(String(255), nullable=True)  # e.g., Stripe charge ID

    # Description
    description = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    processed_at = Column(DateTime, nullable=True)
    settled_at = Column(DateTime, nullable=True)

    # Flags
    is_flagged = Column(Boolean, default=False, nullable=False)
    flag_reason = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Transaction {self.transaction_reference} - {self.type} {self.amount}>"
