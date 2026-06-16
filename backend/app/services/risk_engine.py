"""Risk Scoring Engine - Dynamic fraud detection and AML."""

from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta

from app.models.account import BurnerAccount
from app.models.transaction import Transaction, TransactionStatus
from app.models.risk_score import RiskScore
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RiskEngine:
    """Dynamic risk assessment and fraud detection."""
    
    def calculate_risk_score(
        self,
        account: BurnerAccount,
        db: Session,
    ) -> RiskScore:
        """Calculate comprehensive risk score for an account."""
        
        overall_score = 0
        risk_factors = []
        
        # 1. KYC Risk Score (0-30 points)
        kyc_risk = self._assess_kyc_risk(account)
        overall_score += kyc_risk
        if kyc_risk > 10:
            risk_factors.append("High KYC risk")
        
        # 2. Transaction Velocity (0-25 points)
        velocity_risk = self._assess_transaction_velocity(account, db)
        overall_score += velocity_risk
        if velocity_risk > 10:
            risk_factors.append("High transaction velocity")
        
        # 3. High-Value Transactions (0-25 points)
        high_value_risk = self._assess_high_value_transactions(account, db)
        overall_score += high_value_risk
        if high_value_risk > 10:
            risk_factors.append("High-value transactions detected")
        
        # 4. Geographic Anomaly (0-10 points)
        geo_risk = self._assess_geographic_anomaly(account)
        overall_score += geo_risk
        if geo_risk > 5:
            risk_factors.append("Geographic anomaly detected")
        
        # 5. Pattern Anomaly (0-10 points)
        pattern_risk = self._assess_pattern_anomaly(account, db)
        overall_score += pattern_risk
        if pattern_risk > 5:
            risk_factors.append("Unusual transaction patterns")
        
        # Create risk score record
        is_high_risk = overall_score >= settings.risk_score_threshold
        
        risk_score = RiskScore(
            account_id=account.id,
            overall_score=min(overall_score, 100),
            is_high_risk=is_high_risk,
            kyc_risk_score=kyc_risk,
            transaction_velocity_score=velocity_risk,
            high_value_transaction_score=high_value_risk,
            geographic_anomaly_score=geo_risk,
            pattern_anomaly_score=pattern_risk,
            risk_factors=risk_factors,
        )
        
        # Determine recommended action
        if is_high_risk:
            risk_score.recommended_action = "freeze_account"
        elif overall_score > 50:
            risk_score.recommended_action = "enhanced_due_diligence"
        
        db.add(risk_score)
        db.commit()
        db.refresh(risk_score)
        
        # Update account risk score
        account.risk_score = risk_score.overall_score
        account.is_high_risk = is_high_risk
        db.commit()
        
        logger.info(f"Risk score calculated for {account.id}: {risk_score.overall_score}")
        
        return risk_score
    
    @staticmethod
    def _assess_kyc_risk(account: BurnerAccount) -> int:
        """Assess KYC-related risk (0-30)."""
        score = 0
        
        # New account = higher risk
        account_age = datetime.utcnow() - account.created_at
        if account_age.days < 1:
            score += 15
        elif account_age.days < 7:
            score += 10
        else:
            score += 5
        
        return min(score, 30)
    
    @staticmethod
    def _assess_transaction_velocity(account: BurnerAccount, db: Session) -> int:
        """Assess transaction velocity risk (0-25)."""
        # Count transactions in last hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_transactions = db.query(Transaction).filter(
            Transaction.account_id == account.id,
            Transaction.created_at >= one_hour_ago,
        ).count()
        
        score = 0
        if recent_transactions > 10:
            score = 25
        elif recent_transactions > 5:
            score = 15
        elif recent_transactions > 0:
            score = 5
        
        return score
    
    @staticmethod
    def _assess_high_value_transactions(account: BurnerAccount, db: Session) -> int:
        """Assess high-value transaction risk (0-25)."""
        # Get high-value transactions in configured time window
        time_window = timedelta(hours=settings.high_value_time_window_hours)
        window_start = datetime.utcnow() - time_window
        
        high_value_txns = db.query(Transaction).filter(
            Transaction.account_id == account.id,
            Transaction.amount >= settings.high_value_transaction_limit,
            Transaction.created_at >= window_start,
        ).count()
        
        score = 0
        if high_value_txns > 5:
            score = 25
        elif high_value_txns > 2:
            score = 15
        elif high_value_txns > 0:
            score = 10
        
        return score
    
    @staticmethod
    def _assess_geographic_anomaly(account: BurnerAccount) -> int:
        """Assess geographic anomaly risk (0-10)."""
        # Simplified: just check if IP is available
        score = 0 if account.creation_ip else 5
        return score
    
    @staticmethod
    def _assess_pattern_anomaly(account: BurnerAccount, db: Session) -> int:
        """Assess unusual transaction patterns (0-10)."""
        # Check for suspicious patterns
        transactions = db.query(Transaction).filter(
            Transaction.account_id == account.id
        ).all()
        
        score = 0
        
        # Same amount transactions (potential structuring/smurfing)
        if len(transactions) >= 3:
            amounts = [t.amount for t in transactions]
            if len(set(amounts)) == 1:
                score += 5
        
        # Rapid back-and-forth transfers
        if len(transactions) >= 4:
            recent = transactions[:4]
            types = [t.type for t in recent]
            if types.count("transfer_out") >= 2 and types.count("transfer_in") >= 2:
                score += 5
        
        return min(score, 10)
