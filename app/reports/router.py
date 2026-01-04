from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import PerformanceReport
from app.core.dependencies import get_current_user
from app.models import LedgerTransaction

router = APIRouter()

@router.get("/performance", response_model=List[PerformanceReport])
def get_performance_report(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    # For MVP, a simple placeholder. In a real app, this would involve complex queries
    # to calculate performance metrics from ledger transactions.
    return [
        {
            "date": "2026-01-01",
            "metric": "profit_loss",
            "value": 100.0
        },
        {
            "date": "2026-01-02",
            "metric": "profit_loss",
            "value": 50.0
        }
    ]

