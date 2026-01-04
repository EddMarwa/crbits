from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.schemas import DashboardSummary
from app.core.dependencies import get_current_user
from app.models import LedgerTransaction, UserAllocation, BotPool

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]

    # Calculate invested amount (sum of confirmed deposits)
    invested_amount = db.query(func.sum(LedgerTransaction.amount)).filter(
        LedgerTransaction.user_id == user_id,
        LedgerTransaction.type == "deposit",
        LedgerTransaction.status == "confirmed"
    ).scalar() or 0.0

    # Calculate current value (sum of all confirmed ledger transactions)
    current_value = db.query(func.sum(LedgerTransaction.amount)).filter(
        LedgerTransaction.user_id == user_id,
        LedgerTransaction.status == "confirmed"
    ).scalar() or 0.0

    profit = current_value - invested_amount
    roi = (profit / invested_amount * 100) if invested_amount else 0.0

    return {
        "invested": invested_amount,
        "current_value": current_value,
        "profit": profit,
        "roi": roi
    }

