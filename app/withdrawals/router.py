from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import WithdrawalRequest, LedgerTransactionInDB
from app.core.dependencies import get_current_user
from app.models import LedgerTransaction
from sqlalchemy import func

router = APIRouter()

@router.post("/request", response_model=LedgerTransactionInDB)
def request_withdrawal(withdrawal: WithdrawalRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]

    # Check if user has sufficient funds (sum of confirmed ledger transactions)
    current_balance = db.query(func.sum(LedgerTransaction.amount)).filter(
        LedgerTransaction.user_id == user_id,
        LedgerTransaction.status == "confirmed"
    ).scalar() or 0.0

    if current_balance < withdrawal.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    new_transaction = LedgerTransaction(
        user_id=user_id,
        type="withdrawal",
        amount=-withdrawal.amount, # Withdrawal amounts are negative in the ledger
        currency=withdrawal.currency,
        status="pending" # Requires manual admin approval
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

