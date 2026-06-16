"""Account service - Account management operations."""

from sqlalchemy.orm import Session
import logging
from datetime import datetime

from app.models.account import BurnerAccount, AccountStatus
from app.models.audit import AuditLog

logger = logging.getLogger(__name__)


class AccountService:
    """Service for account operations."""
    
    def close_account(
        self,
        account: BurnerAccount,
        reason: str,
        db: Session,
    ) -> BurnerAccount:
        """Close an account due to expiration or compliance reasons."""
        account.status = AccountStatus.CLOSED
        account.reason_for_closure = reason
        account.closed_at = datetime.utcnow()
        db.commit()
        db.refresh(account)
        
        # Log the closure
        self._log_audit_event(
            event_type="account_closed",
            event_description=f"Account closed: {reason}",
            account_id=account.id,
            db=db,
        )
        
        logger.info(f"Account {account.id} closed: {reason}")
        return account
    
    def freeze_account(
        self,
        account: BurnerAccount,
        reason: str,
        db: Session,
    ) -> BurnerAccount:
        """Freeze an account for compliance review."""
        account.status = AccountStatus.FROZEN
        account.is_flagged_for_review = True
        db.commit()
        db.refresh(account)
        
        self._log_audit_event(
            event_type="account_frozen",
            event_description=f"Account frozen: {reason}",
            account_id=account.id,
            db=db,
        )
        
        logger.warning(f"Account {account.id} frozen: {reason}")
        return account
    
    def activate_account(
        self,
        account: BurnerAccount,
        db: Session,
    ) -> BurnerAccount:
        """Activate an account after KYC verification."""
        account.status = AccountStatus.ACTIVE
        db.commit()
        db.refresh(account)
        
        self._log_audit_event(
            event_type="account_activated",
            event_description="Account activated after KYC verification",
            account_id=account.id,
            db=db,
        )
        
        logger.info(f"Account {account.id} activated")
        return account
    
    @staticmethod
    def _log_audit_event(
        event_type: str,
        event_description: str,
        account_id: str,
        db: Session,
    ) -> None:
        """Log an audit event."""
        audit_log = AuditLog(
            event_type=event_type,
            event_description=event_description,
            account_id=account_id,
        )
        db.add(audit_log)
        db.commit()
