"""Account endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models.account import BurnerAccount
from app.schemas.account import (
    CreateBurnerAccountRequest,
    BurnerAccountResponse,
    AccountDetailResponse,
    KYCSubmissionRequest,
    KYCVerificationResponse,
)
from app.services.account_service import AccountService
from app.services.kyc_service import KYCService
from app.utils import generate_account_number, generate_routing_number

logger = logging.getLogger(__name__)
router = APIRouter()

account_service = AccountService()
kyc_service = KYCService()


@router.post("/create", response_model=BurnerAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_burner_account(
    request: CreateBurnerAccountRequest,
    db: Session = Depends(get_db),
):
    """
    Create a temporary burner account.
    
    The account will have a Time-To-Live (TTL) and must pass KYC verification
    before it can be used for transactions.
    """
    try:
        # Generate account identifiers
        account_number = generate_account_number()
        routing_number = generate_routing_number()
        
        # Create account
        account = BurnerAccount(
            account_number=account_number,
            routing_number=routing_number,
            account_holder_name=request.account_holder_name,
            ttl_days=request.ttl_days,
            creation_ip=request.creation_ip,
            creation_device_fingerprint=request.creation_device_fingerprint,
        )
        
        db.add(account)
        db.commit()
        db.refresh(account)
        
        logger.info(f"Burner account created: {account.account_number}")
        
        return BurnerAccountResponse.model_validate(account)
    except Exception as e:
        logger.error(f"Failed to create burner account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create burner account"
        )


@router.get("/{account_id}", response_model=AccountDetailResponse)
async def get_account(
    account_id: str,
    db: Session = Depends(get_db),
):
    """Get detailed account information."""
    account = db.query(BurnerAccount).filter(BurnerAccount.id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return AccountDetailResponse.model_validate(account)


@router.post("/{account_id}/kyc/submit", response_model=KYCVerificationResponse)
async def submit_kyc(
    account_id: str,
    request: KYCSubmissionRequest,
    db: Session = Depends(get_db),
):
    """
    Submit KYC verification for an account.
    
    This will initiate verification through the sandbox KYC provider (Onfido).
    """
    # Verify account exists
    account = db.query(BurnerAccount).filter(BurnerAccount.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    try:
        # Submit KYC
        kyc_verification = await kyc_service.submit_kyc(
            account_id=account_id,
            request=request,
            db=db,
        )
        
        return KYCVerificationResponse.model_validate(kyc_verification)
    except Exception as e:
        logger.error(f"Failed to submit KYC for account {account_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit KYC verification"
        )


@router.get("/{account_id}/kyc/status", response_model=KYCVerificationResponse)
async def get_kyc_status(
    account_id: str,
    db: Session = Depends(get_db),
):
    """Get KYC verification status for an account."""
    kyc_verification = await kyc_service.get_kyc_status(account_id, db)
    
    if not kyc_verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No KYC verification found for this account"
        )
    
    return KYCVerificationResponse.model_validate(kyc_verification)


@router.post("/{account_id}/freeze")
async def freeze_account(
    account_id: str,
    db: Session = Depends(get_db),
):
    """Freeze an account for risk or compliance reasons."""
    account = db.query(BurnerAccount).filter(BurnerAccount.id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    try:
        from app.models.account import AccountStatus
        account.status = AccountStatus.FROZEN
        db.commit()
        
        logger.info(f"Account frozen: {account_id}")
        
        return {"status": "Account frozen successfully"}
    except Exception as e:
        logger.error(f"Failed to freeze account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to freeze account"
        )
