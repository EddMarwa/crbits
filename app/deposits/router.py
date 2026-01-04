from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import DepositConfirm, LedgerTransactionInDB
from app.core.dependencies import get_current_user
from app.models import LedgerTransaction

router = APIRouter()

@router.post("/confirm", response_model=LedgerTransactionInDB)
def confirm_deposit(deposit: DepositConfirm, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    
    # In a real system, this would involve integrating with a payment gateway
    # and then confirming the deposit. For MVP, we directly create a pending transaction.
    new_transaction = LedgerTransaction(
        user_id=user_id,
        type="deposit",
        amount=deposit.amount,
        currency=deposit.currency,
        reference=deposit.reference,
        status="pending" # Manual admin approval is required for withdrawals, deposits are confirmed here for MVP simplicity
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # For deposits, the status can be directly confirmed for MVP, assuming it's a simulated payment.
    # For actual integration, this would be a webhook callback.
    new_transaction.status = "confirmed"
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

