"""Transaction endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from app.database import get_db
from app.models.account import BurnerAccount, AccountStatus
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.account import TransactionRequest, TransactionResponse
from app.utils import generate_account_number
from app.utils.security import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.post("/{account_id}/submit", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def submit_transaction(
    account_id: str,
    request: TransactionRequest,
    db: Session = Depends(get_db),
):
    """
    Submit a transaction for an account.
    
    Transaction will be subject to risk scoring and compliance checks.
    """
    # Verify account exists and is active
    account = db.query(BurnerAccount).filter(BurnerAccount.id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    if account.status not in [AccountStatus.ACTIVE]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account is {account.status}, cannot process transactions"
        )
    
    if account.is_expired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account has expired"
        )
    
    try:
        # Create transaction
        transaction = Transaction(
            account_id=account_id,
            type=request.type,
            amount=request.amount,
            counterparty_name=request.counterparty_name,
            counterparty_account=request.counterparty_account,
            counterparty_routing=request.counterparty_routing,
            description=request.description,
            transaction_reference=generate_account_number(),  # Use for now
            status=TransactionStatus.PENDING,
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Transaction submitted: {transaction.transaction_reference}")
        
        return TransactionResponse.model_validate(transaction)
    except Exception as e:
        logger.error(f"Failed to submit transaction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit transaction"
        )


@router.get("/{account_id}/history", response_model=list[TransactionResponse])
async def get_transaction_history(
    account_id: str,
    db: Session = Depends(get_db),
):
    """Get transaction history for an account."""
    # Verify account exists
    account = db.query(BurnerAccount).filter(BurnerAccount.id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    try:
        transactions = db.query(Transaction).filter(
            Transaction.account_id == account_id
        ).order_by(Transaction.created_at.desc()).all()
        
        return [TransactionResponse.model_validate(t) for t in transactions]
    except Exception as e:
        logger.error(f"Failed to retrieve transaction history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve transaction history"
        )
