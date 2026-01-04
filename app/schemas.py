from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: UUID
    role: str
    kyc_status: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[UUID] = None

class BotBase(BaseModel):
    name: str
    risk_level: Optional[str] = None
    active: bool = True

class BotCreate(BotBase):
    pass

class BotInDB(BotBase):
    id: UUID

    class Config:
        from_attributes = True

class BotPoolInDB(BaseModel):
    bot_id: UUID
    total_capital: float
    last_pnl_at: str

    class Config:
        from_attributes = True

class UserAllocationBase(BaseModel):
    bot_id: UUID
    amount: float

class UserAllocationCreate(UserAllocationBase):
    pass

class UserAllocationInDB(UserAllocationBase):
    user_id: UUID

    class Config:
        from_attributes = True

class LedgerTransactionBase(BaseModel):
    type: str
    amount: float
    currency: str
    reference: Optional[str] = None
    status: str

class LedgerTransactionCreate(LedgerTransactionBase):
    pass

class LedgerTransactionInDB(LedgerTransactionBase):
    id: UUID
    user_id: UUID
    created_at: str # will be datetime

    class Config:
        from_attributes = True

class DepositConfirm(BaseModel):
    amount: float
    currency: str
    reference: Optional[str] = None

class WithdrawalRequest(BaseModel):
    amount: float
    currency: str

class AdminWithdrawalApproval(BaseModel):
    status: str # approved, rejected

class DashboardSummary(BaseModel):
    invested: float
    current_value: float
    profit: float
    roi: float

class PerformanceReport(BaseModel):
    date: str
    metric: str
    value: float

