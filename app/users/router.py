from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import UserInDB
from app.core.dependencies import get_current_user, get_db
from app.models import User

router = APIRouter()

@router.get("/me", response_model=UserInDB)
def read_users_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    return user

