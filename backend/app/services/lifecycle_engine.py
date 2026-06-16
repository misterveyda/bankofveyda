"""Account Lifecycle Engine - TTL expiration and cleanup."""

from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta

from app.models.account import BurnerAccount, AccountStatus
from app.models.transaction import Transaction, TransactionType, TransactionStatus
from app.models.audit import AuditLog
from app.config import get_settings
from app.utils import generate_account_number

logger = logging.getLogger(__name__)
settings = get_settings()


class LifecycleEngine:
    """Manages account lifecycle: creation, expiration, cleanup."""
    
    def cleanup_expired_accounts(self, db: Session) -> dict:
        """
        Scan for expired accounts and enforce closure protocols.
        
        This is the core of the compliance simulator - showing why
        temporary accounts must comply with strict regulations.
        """
        results = {
            "expired_found": 0,
            "closed": 0,
            "funds_returned": 0,
            "errors": 0,
        }
        
        try:
            # Find expired accounts that aren't already closed
            expired_accounts = db.query(BurnerAccount).filter(
                BurnerAccount.expires_at <= datetime.utcnow(),
                BurnerAccount.status != AccountStatus.CLOSED,
            ).all()
            
            results["expired_found"] = len(expired_accounts)
            
            for account in expired_accounts:
                try:
                    # 1. Freeze the account
                    account.status = AccountStatus.FROZEN
                    
                    # 2. Return remaining balance to source (if applicable)
                    if account.balance > 0:
                        return_txn = Transaction(
                            account_id=account.id,
                            type=TransactionType.CLOSURE_RETURN,
                            amount=account.balance,
                            description="Automatic return on account closure",
                            transaction_reference=generate_account_number(),
                            status=TransactionStatus.COMPLETED,
                        )
                        db.add(return_txn)
                        results["funds_returned"] += 1
                        account.balance = 0.0
                    
                    # 3. Mark as closed
                    account.status = AccountStatus.CLOSED
                    account.reason_for_closure = "TTL expired - automatic closure"
                    account.closed_at = datetime.utcnow()
                    
                    # 4. Log audit event
                    audit_log = AuditLog(
                        event_type="account_expired",
                        event_description=f"Account expired after {account.ttl_days} days",
                        account_id=account.id,
                        severity="INFO",
                    )
                    db.add(audit_log)
                    
                    results["closed"] += 1
                    logger.info(f"Cleaned up expired account: {account.id}")
                    
                except Exception as e:
                    logger.error(f"Error cleaning up account {account.id}: {str(e)}")
                    results["errors"] += 1
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error in cleanup_expired_accounts: {str(e)}")
            results["errors"] += 1
        
        logger.info(f"Cleanup completed: {results}")
        return results
    
    def check_expiring_soon(self, days_until: int = 3) -> list[BurnerAccount]:
        """
        Get accounts expiring within N days for proactive notifications.
        """
        db = Session()
        try:
            expiry_threshold = datetime.utcnow() + timedelta(days=days_until)
            
            expiring_accounts = db.query(BurnerAccount).filter(
                BurnerAccount.expires_at <= expiry_threshold,
                BurnerAccount.expires_at > datetime.utcnow(),
                BurnerAccount.status != AccountStatus.CLOSED,
            ).all()
            
            return expiring_accounts
        finally:
            db.close()
