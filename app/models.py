import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(Text, unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, default="user")
    kyc_status = Column(Text, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ledger_transactions = relationship("LedgerTransaction", back_populates="user")
    user_allocations = relationship("UserAllocation", back_populates="user")

class Bot(Base):
    __tablename__ = "bots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    risk_level = Column(Text)
    active = Column(Boolean, default=True)

    user_allocations = relationship("UserAllocation", back_populates="bot")
    bot_pool = relationship("BotPool", back_populates="bot", uselist=False)

class BotPool(Base):
    __tablename__ = "bot_pools"

    bot_id = Column(UUID(as_uuid=True), ForeignKey("bots.id"), primary_key=True)
    total_capital = Column(Numeric(18, 8), nullable=False, default=0.0)
    last_pnl_at = Column(DateTime(timezone=True), server_default=func.now())

    bot = relationship("Bot", back_populates="bot_pool")

class UserAllocation(Base):
    __tablename__ = "user_allocations"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    bot_id = Column(UUID(as_uuid=True), ForeignKey("bots.id"), primary_key=True)
    amount = Column(Numeric(18, 8), nullable=False)

    user = relationship("User", back_populates="user_allocations")
    bot = relationship("Bot", back_populates="user_allocations")

class LedgerTransaction(Base):
    __tablename__ = "ledger_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Text, nullable=False)
    amount = Column(Numeric(18, 8), nullable=False)
    currency = Column(Text, nullable=False)
    reference = Column(Text)
    status = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="ledger_transactions")

