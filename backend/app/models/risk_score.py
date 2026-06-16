"""RiskScore model - Dynamic risk assessment."""

from sqlalchemy import Column, String, Integer, DateTime, Float, Text, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.database import Base


class RiskScore(Base):
    """
    Dynamic risk scoring for fraud detection and AML compliance.
    Demonstrates how banks identify suspicious patterns.
    """

    __tablename__ = "risk_scores"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Key
    account_id = Column(String(36), ForeignKey("burner_accounts.id"), nullable=False, index=True)

    # Risk Scoring
    overall_score = Column(Integer, nullable=False)  # 0-100
    is_high_risk = Column(Boolean, default=False, nullable=False)

    # Risk Factors (breakdown)
    kyc_risk_score = Column(Integer, default=0)
    transaction_velocity_score = Column(Integer, default=0)
    high_value_transaction_score = Column(Integer, default=0)
    geographic_anomaly_score = Column(Integer, default=0)
    pattern_anomaly_score = Column(Integer, default=0)

    # Risk Details
    risk_factors = Column(JSON, nullable=True)  # List of detected risk factors
    risk_rules_triggered = Column(JSON, nullable=True)  # Which rules caused the risk assessment

    # Recommended Actions
    recommended_action = Column(String(100), nullable=True)  # e.g., "freeze_account", "enhanced_due_diligence"
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    review_notes = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<RiskScore {self.account_id} - Score: {self.overall_score}>"
