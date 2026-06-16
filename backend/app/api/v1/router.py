"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import accounts, transactions

router = APIRouter()

# Include endpoint routers
router.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
