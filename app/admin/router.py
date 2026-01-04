from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.schemas import LedgerTransactionInDB, AdminWithdrawalApproval
from app.core.dependencies import get_admin_user # Assuming you'll have an admin dependency
from app.models import LedgerTransaction

router = APIRouter()

@router.post("/withdrawals/{transaction_id}/approve", response_model=LedgerTransactionInDB)
def approve_withdrawal(transaction_id: UUID, approval: AdminWithdrawalApproval, db: Session = Depends(get_db), admin_user: dict = Depends(get_admin_user)):
    transaction = db.query(LedgerTransaction).filter(LedgerTransaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    if transaction.type != "withdrawal" or transaction.status != "pending":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction for approval")
    
    transaction.status = approval.status
    db.commit()
    db.refresh(transaction)
    return transaction

