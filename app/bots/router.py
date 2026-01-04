from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import BotInDB, UserAllocationCreate
from app.core.dependencies import get_current_user
from app.models import Bot, UserAllocation, BotPool

router = APIRouter()

@router.get("/", response_model=List[BotInDB])
def get_bots(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # In a real app, you might filter bots based on user or other criteria
    bots = db.query(Bot).filter(Bot.active == True).all()
    return bots

@router.post("/allocate", response_model=UserAllocationCreate)
def allocate_to_bot(allocation: UserAllocationCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Check if the bot exists
    bot = db.query(Bot).filter(Bot.id == allocation.bot_id, Bot.active == True).first()
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot not found or inactive")
    
    # Check if user already allocated to this bot
    user_id = current_user["id"]
    user_allocation = db.query(UserAllocation).filter(
        UserAllocation.user_id == user_id,
        UserAllocation.bot_id == allocation.bot_id
    ).first()

    if user_allocation:
        user_allocation.amount += allocation.amount
    else:
        user_allocation = UserAllocation(
            user_id=user_id,
            bot_id=allocation.bot_id,
            amount=allocation.amount
        )
        db.add(user_allocation)
    
    # Update BotPool total_capital
    bot_pool = db.query(BotPool).filter(BotPool.bot_id == allocation.bot_id).first()
    if bot_pool:
        bot_pool.total_capital += allocation.amount
    else:
        new_bot_pool = BotPool(bot_id=allocation.bot_id, total_capital=allocation.amount)
        db.add(new_bot_pool)

    db.commit()
    db.refresh(user_allocation)
    # Refresh bot_pool if it exists, or the newly created one
    if bot_pool:
        db.refresh(bot_pool)
    else:
        db.refresh(new_bot_pool)
    return allocation

