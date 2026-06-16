"""Additional schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class RiskScoreResponse(BaseModel):
    """Risk score assessment response."""
    id: str
    account_id: str
    overall_score: int
    is_high_risk: bool
    kyc_risk_score: int
    transaction_velocity_score: int
    high_value_transaction_score: int
    geographic_anomaly_score: int
    pattern_anomaly_score: int
    risk_factors: Optional[List[str]] = None
    recommended_action: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    database: str
    timestamp: datetime


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[Any]
