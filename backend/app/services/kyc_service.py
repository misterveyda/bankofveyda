"""KYC Service - Identity verification operations."""

from sqlalchemy.orm import Session
import logging
from datetime import datetime
import httpx

from app.models.kyc import KYCVerification, VerificationStatus, VerificationProvider
from app.models.account import BurnerAccount, AccountStatus
from app.schemas.account import KYCSubmissionRequest
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class KYCService:
    """Service for KYC verification operations."""
    
    async def submit_kyc(
        self,
        account_id: str,
        request: KYCSubmissionRequest,
        db: Session,
    ) -> KYCVerification:
        """Submit KYC verification through Onfido sandbox."""
        
        # Create KYC record
        kyc = KYCVerification(
            account_id=account_id,
            provider=VerificationProvider.ONFIDO,
            full_name=request.full_name,
            date_of_birth=request.date_of_birth,
            country=request.country,
            document_type=request.document_type,
            document_number=request.document_number,
            document_expiry=request.document_expiry,
            status=VerificationStatus.SUBMITTED,
        )
        
        try:
            # For sandbox, simulate verification
            kyc.provider_check_id = f"check_{account_id[:8]}"
            kyc.is_verified = True
            kyc.verification_timestamp = datetime.utcnow()
            kyc.status = VerificationStatus.APPROVED
            
            # Update account status
            account = db.query(BurnerAccount).filter(BurnerAccount.id == account_id).first()
            if account:
                account.status = AccountStatus.ACTIVE
            
            db.add(kyc)
            db.commit()
            db.refresh(kyc)
            
            logger.info(f"KYC verification approved for account {account_id}")
            
        except Exception as e:
            logger.error(f"Failed to submit KYC: {str(e)}")
            kyc.status = VerificationStatus.REJECTED
            kyc.failure_reason = str(e)
            db.add(kyc)
            db.commit()
            db.refresh(kyc)
        
        return kyc
    
    async def get_kyc_status(
        self,
        account_id: str,
        db: Session,
    ) -> KYCVerification:
        """Get KYC verification status."""
        kyc = db.query(KYCVerification).filter(
            KYCVerification.account_id == account_id
        ).order_by(KYCVerification.created_at.desc()).first()
        
        return kyc
    
    async def _call_onfido_api(
        self,
        endpoint: str,
        method: str = "POST",
        payload: dict = None,
    ) -> dict:
        """Call Onfido API (sandbox)."""
        url = f"{settings.onfido_sandbox_url}/{endpoint}"
        headers = {
            "Authorization": f"Token token={settings.onfido_api_token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                if method == "POST":
                    response = await client.post(url, json=payload, headers=headers)
                else:
                    response = await client.get(url, headers=headers)
                
                return response.json()
        except Exception as e:
            logger.error(f"Onfido API call failed: {str(e)}")
            raise
