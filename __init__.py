"""
Trading Account Management Platform

A robust platform for managing trading accounts with deposit and withdrawal functionality.
"""

from .trading_account import (
    TradingAccount,
    TradingPlatform,
    Transaction,
    InsufficientFundsError,
    InvalidAmountError
)

__version__ = '1.0.0'
__all__ = [
    'TradingAccount',
    'TradingPlatform',
    'Transaction',
    'InsufficientFundsError',
    'InvalidAmountError'
]
