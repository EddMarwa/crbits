from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import LedgerTransactionInDB
from app.core.dependencies import get_current_user
from app.models import LedgerTransaction

router = APIRouter()

@router.get("/history", response_model=List[LedgerTransactionInDB])
def get_ledger_history(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    transactions = db.query(LedgerTransaction).filter(LedgerTransaction.user_id == user_id).order_by(LedgerTransaction.created_at.desc()).all()
    return transactions

