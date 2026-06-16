"""Celery background workers for account lifecycle management."""

from celery import Celery
from app.config import get_settings
from app.database import SessionLocal
from app.services.lifecycle_engine import LifecycleEngine
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "bankofveyda",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="cleanup_expired_accounts")
def cleanup_expired_accounts():
    """
    Scheduled task: Clean up expired accounts every hour.
    
    This enforces the TTL (Time-To-Live) compliance requirement.
    """
    db = SessionLocal()
    try:
        lifecycle_engine = LifecycleEngine()
        results = lifecycle_engine.cleanup_expired_accounts(db)
        logger.info(f"Account cleanup completed: {results}")
        return results
    except Exception as e:
        logger.error(f"Error in cleanup task: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(name="recalculate_risk_scores")
def recalculate_risk_scores():
    """
    Scheduled task: Recalculate risk scores for all active accounts.
    """
    from app.models.account import BurnerAccount, AccountStatus
    from app.services.risk_engine import RiskEngine
    
    db = SessionLocal()
    try:
        # Get all active accounts
        accounts = db.query(BurnerAccount).filter(
            BurnerAccount.status == AccountStatus.ACTIVE
        ).all()
        
        risk_engine = RiskEngine()
        updated_count = 0
        
        for account in accounts:
            try:
                risk_engine.calculate_risk_score(account, db)
                updated_count += 1
            except Exception as e:
                logger.error(f"Error calculating risk for {account.id}: {str(e)}")
        
        logger.info(f"Risk scores recalculated for {updated_count} accounts")
        return {"updated": updated_count, "total": len(accounts)}
        
    except Exception as e:
        logger.error(f"Error in risk score recalculation: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(name="send_expiration_notifications")
def send_expiration_notifications():
    """
    Scheduled task: Send notifications for accounts expiring soon.
    """
    db = SessionLocal()
    try:
        lifecycle_engine = LifecycleEngine()
        expiring_accounts = lifecycle_engine.check_expiring_soon(days_until=3)
        
        # In production, send email/SMS notifications here
        logger.info(f"Found {len(expiring_accounts)} accounts expiring soon")
        
        return {"expiring_soon": len(expiring_accounts)}
        
    except Exception as e:
        logger.error(f"Error sending notifications: {str(e)}")
        raise
    finally:
        db.close()
